import datetime
import json
import logging
import random
import sys
import time

sys.path.insert(0, '../broker/')

import pandas as pd
from producer import run_kafka_producer
from pyModbusTCP.client import ModbusClient

host = "localhost"

def read_csv (csvfile: str) -> pd.DataFrame:
    df = pd.read_csv(csvfile, sep=',', header='infer')
    return df

def configure (): 
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='iot-messor.log',
                        maxBytes=5*1024*1024,
                        backupCount=5,
                        filemode='w')

    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
def modbus_read(modbus_client: ModbusClient, df: pd.DataFrame) -> dict:
    if modbus_client is None:
        print("modbus_read: modbus_client is None!\n")
        return None
      
    if df is None:
        print("modbus_read: Dataframe is None!\n")
        return None

    # store dataframe in a list 
    list_result = []

    for reg_num in range(35, 102):
        reg = df.loc[df['Endereço'] == reg_num]
        if not reg.empty:
            df_dict = {}
            df_dict['Endereço'] = reg['Endereço'].values[0]
            df_dict['Registrador'] = reg['Registrador'].values[0]
            df_dict['Range'] = reg['Range'].values[0]
            df_dict['Unidade'] = reg['Unidade'].values[0]
            df_dict['Tipo / Função'] = reg['Tipo / Função'].values[0]

            reg_mapmem = modbus_client.read_holding_registers(reg_num, 1)

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

def run_messor(
  modbus_host: str = "192.168.1.1", 
  port: int = 502,
  csv_file: str = "modbus-mapa-memoria.csv", 
  csv_file_result: str = "modbus-mapa-memoria-result.csv"): 

  configure()
  
  logger.info('Reading CSV file: [{}]'.format(csv_file))
  df = read_csv(csv_file)
  if df is not None:
    logger.info(df)

    # create modbus client
    logger.info('Creating Modbus client...')
    modbus_client = ModbusClient(host=modbus_host, port=port, unit_id=1, auto_open=True)

    if not modbus_client.open():
      logger.error('Unable to connect to host: [{}], port: [{}]. End of execution.'.format(modbus_host,port))
    else:
      list_memmaps = modbus_read(modbus_client, df)

      if list_memmaps is not None:
          with open(csv_file_result, 'a') as f:
              # write header
              f.write('Timestamp,Device,Endereço,Registrador,Range,Unidade,Tipo / Função,Valor')
              f.write('\n')

              while True:
                print ("=============================")
                print ("MODBUS:: READ MEMORY MAP VALUES:")
                logger.info("MODBUS:: READ MEMORY MAP VALUES:")
                
                broker_dict = {}
                for memmap in list_memmaps:
                    record_dict = {}
                  
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
                    
                    logger.info("=============================")

                    logger.info('Memory Map number #{}: '.format(memmap['Endereço']))
                    logger.info('\tRegistrador: {}'.format(memmap['Registrador']))
                    logger.info('\tTipo / Função: {}'.format(memmap['Tipo / Função']))
                    logger.info('\tRange: {}'.format(memmap['Range']))
                    logger.info('\tUnidade: {}'.format(memmap['Unidade']))
                    logger.info('\tValor: {}'.format(memmap['Valor']))
                    
                    print("=============================")

                    print('Memory Map number #{}: '.format(memmap['Endereço']))
                    print('\tRegistrador: {}'.format(memmap['Registrador']))
                    print('\tTipo / Função: {}'.format(memmap['Tipo / Função']))
                    print('\tRange: {}'.format(memmap['Range']))
                    print('\tUnidade: {}'.format(memmap['Unidade']))
                    print('\tValor: {}'.format(memmap['Valor']))
                    
                    record_dict['timestamp'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    record_dict['device'] = 'messor'
                    record_dict['Endereco'] = str(memmap['Endereço'])
                    record_dict['Registrador'] = memmap['Registrador']
                    record_dict['Range'] = memmap['Range']
                    record_dict['Unidade'] = memmap['Unidade']
                    record_dict['Tipo / Função'] = memmap['Tipo / Função']
                    record_dict['Valor'] = str(memmap['Valor'])
                    
                    # append to broker list
                    print (record_dict)
                    broker_dict[str(memmap['Endereço'])] = record_dict

                logger.info("=============================")
                print("=============================")

                run_kafka_producer(data_dict=broker_dict)
                time.sleep(5)

          f.close()
          logger.info("MODBUS:: READ MEMORY MAP FINISHED!")

      else:
          logger.error("MODBUS:: READ MEMORY MAP ERROR. End of execution.")
  else:
    logger.error('Unable to read CSV file: [{}]. End of execution.'.format(csv_file))

if __name__ == "__main__":
  run_messor()


