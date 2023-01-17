import datetime
import logging
import sys
import time

sys.path.insert(0, '../broker/')

import pandas as pd
from producer import run_kafka_producer, set_show_broker_producer_logs
from pyModbusTCP.client import ModbusClient

show_messor_logs = True
def set_show_messor_logs(value : bool):
  global show_messor_logs
  show_messor_logs = value

logger = None
def read_csv (csvfile: str) -> pd.DataFrame:
  df = pd.read_csv(csvfile, sep=',', header='infer')
  return df

def create_logger (filename: str = 'iot-messor.log'): 
  global logger
  if logger is not None:
    return
  
  logging.basicConfig(format='%(asctime)s %(message)s',
                      datefmt='%Y-%m-%d %H:%M:%S',
                      filename=filename,
                      filemode='w')

  logger = logging.getLogger()
  logger.setLevel(logging.INFO)
    
def log (message, type = 'info'):
  if show_messor_logs:
    if type == 'error':
        logger.error(message)
        print ('Error: {}'.format(message))
    else:
        logger.info(message)
        print ('Info: {}'.format(message))
        
def configure(show_producer_logs: bool = False, show_messor_logs: bool = False):
  set_show_broker_producer_logs (show_producer_logs)
  set_show_messor_logs (show_messor_logs)

  configure_dict = {
    'modbus_host': '192.168.1.1',
    'port': 502,
    'csv_file': 'modbus-mapa-memoria.csv',
    'csv_file_result': 'modbus-mapa-memoria-result.csv',
    'num_cycles': 1,
    'kafka_host': 'localhost',
    'kafka_port': 9092,
    'kafka_topic': 'iot-topic'
  }

  # get information from program arguments
  if len(sys.argv) > 1:
    if sys.argv[1] != "-": configure_dict['modbus_host'] = sys.argv[1]
    if sys.argv[2] != "-": configure_dict['port'] = int(sys.argv[2])
    if sys.argv[3] != "-": configure_dict['csv_file'] = sys.argv[3]
    if sys.argv[4] != "-": configure_dict['csv_file_result'] = sys.argv[4]
    if sys.argv[5] != "-": configure_dict['num_cycles'] = int(sys.argv[5])

  configure_dict['df_sensors'] = read_csv(configure_dict['csv_file'])
  if configure_dict['df_sensors'] is not None:
    logger.info('Reading CSV file: [{}]\n{}'.format(
      configure_dict['csv_file'], configure_dict['df_sensors']))

    configure_dict['modbus_client'] = ModbusClient(
      host=configure_dict['modbus_host'], port=configure_dict['port'], 
      unit_id=1, auto_open=True)
  else:
    logger.error('Unable to read CSV file: [{}]. End of execution.'.format(configure_dict['csv_file']))
    return None
  
  return configure_dict


def modbus_read(configure_dict : dict) -> dict:
  if configure_dict['modbus_client'] is None:
      log("modbus_read: modbus_client is None!\n")
      return None
    
  if configure_dict['df_sensors'] is None:
      log("modbus_read: Dataframe is None!\n")
      return None

  # store dataframe in a list 
  list_result = []

  for reg_num in range(35, 102):
      reg = configure_dict['df_sensors'].loc[configure_dict['df_sensors']['Endereço'] == reg_num]
      if not reg.empty:
          df_dict = {}
          df_dict['Endereço'] = reg['Endereço'].values[0]
          df_dict['Registrador'] = reg['Registrador'].values[0]
          df_dict['Range'] = reg['Range'].values[0]
          df_dict['Unidade'] = reg['Unidade'].values[0]
          df_dict['Tipo / Função'] = reg['Tipo / Função'].values[0]

          reg_mapmem = configure_dict['modbus_client'].read_holding_registers(reg_num, 1)

          if reg_mapmem is not None:
            df_dict['Valor'] = reg_mapmem[0]
          else:
            print("Read error at maemory map location #" + str(reg_num))
            df_dict['Valor'] = None
          
          list_result.append(df_dict)

  if len(list_result) > 0:
      return list_result
  else:
      print("modbus_read: General read error (result list is empty)!\n")
      return None

def save_csv(configure_dict: dict, list_memmaps: list):
  with open(configure_dict['csv_file_result'], 'a') as f:
    f.write('Timestamp,Device,Endereço,Registrador,Range,Unidade,Tipo / Função,Valor')
    f.write('\n')

    for memmap in list_memmaps:
      f.write(
        str(time.time()) + ',' +
        'messor' + ',' +
        str(memmap['Endereço']) + ',' + 
        memmap['Registrador'] + ',' + 
        memmap['Range'] + ',' + 
        memmap['Unidade'] + ',' + 
        memmap['Tipo / Função'] + ',' + 
        str(memmap['Valor']))
      f.write('\n')

    f.close()
      
def report(configure_dict: dict, list_memmaps: list):
  log ('=============================')
  log ('READ MODBUS MEMORY MAP VALUES:')
  
  log('\nArguments summary:\v')
  log('\tModbus host: [{}]'.format(configure_dict['modbus_host']))
  log('\tPort: [{}]'.format(configure_dict['port']))
  log('\tCSV file: [{}]'.format(configure_dict['csv_file']))
  log('\tCSV file result: [{}]'.format(configure_dict['csv_file_result']))
  log('\tNumber of cycles: [{}]'.format(configure_dict['num_cycles']))
  log('\tKafka host: [{}]'.format(configure_dict['kafka_host']))
  log('\tKafka port: [{}]'.format(configure_dict['kafka_port']))
  log('\tKafka topic: [{}]'.format(configure_dict['kafka_topic']))
  log('\tModbus client: [{}]'.format(configure_dict['modbus_client']))
  log('df_sensors:\n{}'.format(configure_dict['df_sensors']))

  for memmap in list_memmaps:
    if memmap is None:
      log('report: memmap is None!', 'error')
      return
  
    log("=============================")
    log('Memory Map number #{}: '.format(memmap['Endereço']))
    log('\tRegistrador: {}'.format(memmap['Registrador']))
    log('\tTipo / Função: {}'.format(memmap['Tipo / Função']))
    log('\tRange: {}'.format(memmap['Range']))
    log('\tUnidade: {}'.format(memmap['Unidade']))
    log('\tValor: {}'.format(memmap['Valor']))

  log("MODBUS:: READ MEMORY MAP FINISHED!")

def run_messor(configure_dict: dict):
  log('=============================')
  log('Messor Modbus Client started.')
  log('=============================')
  
  if not configure_dict['modbus_client'].open():
    log('Unable to connect to host: [{}], port: [{}]. End of execution!'.format(
      configure_dict['modbus_host'], configure_dict['port']), 'error')
    return None
  else:
    list_memmaps = modbus_read(configure_dict)
    
    timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    if list_memmaps is not None:
      broker_dict = {}
      for memmap in list_memmaps:
        record_dict = {}
      
        record_dict['timestamp'] = timestamp
        record_dict['device'] = 'messor'
        record_dict['Endereco'] = str(memmap['Endereço'])
        record_dict['Registrador'] = memmap['Registrador']
        record_dict['Range'] = memmap['Range']
        record_dict['Unidade'] = memmap['Unidade']
        record_dict['Tipo / Função'] = memmap['Tipo / Função']
        record_dict['Valor'] = str(memmap['Valor'])
        
        # append to broker list
        broker_dict[str(memmap['Endereço'])] = record_dict

      run_kafka_producer(data_dict=broker_dict)
      
      log('=============================')
      log('Messor Modbus Client ended.')
      log('=============================')

      return list_memmaps
    else:
        log("MODBUS:: READ ERROR. End of execution.", 'error')
        return None
  

def main ():
  create_logger()
  configure_dict = configure()
  list_memmaps = run_messor(configure_dict)
  if list_memmaps is not None and show_messor_logs:
    report (configure_dict, list_memmaps)

if __name__ == "__main__":
  main()


