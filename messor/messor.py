import time
from pyModbusTCP.client import ModbusClient
import pandas as pd

host = "localhost"
port = 502

modbus_host = "192.168.1.1"
csv_file = "modbus-mapa-memoria.csv"
csv_file_result = "modbus-mapa-memoria-result.csv"

def read_csv (csvfile: str) -> pd.DataFrame:
    df = pd.read_csv(csvfile, sep=',', header='infer')
    return df

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
            # store dataframe in a list
            df_dict = {}
            df_dict['Endereço'] = reg['Endereço'].values[0]
            df_dict['Registrador'] = reg['Registrador'].values[0]
            df_dict['Range'] = reg['Range'].values[0]
            df_dict['Unidade'] = reg['Unidade'].values[0]
            df_dict['Tipo / Função'] = reg['Tipo / Função'].values[0]

            # read modbus register
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

def main():
  print('Reading CSV file: [{}]'.format(csv_file))
  df = read_csv(csv_file)
  if df is not None:
    print(df)
    print()

    # create modbus client
    modbus_client = ModbusClient(host=modbus_host, port=port, unit_id=1, auto_open=True)

    if not modbus_client.open():
      print('Unable to connect to host: [{}], port: [{}]. End of execution.'.format(modbus_host,port))
    else:
      list_memmaps = modbus_read(modbus_client, df)

      if list_memmaps is not None:
          print("\nMODBUS:: READ MEMORY MAP VALUES:\n")

          # open csv file to write
          with open(csv_file_result, 'w') as f:
              # write header
              f.write('Endereço,Registrador,Range,Unidade,Tipo / Função,Valor')
              f.write('\n')

              # write values

              for memmap in list_memmaps:
                  f.write(
                    str(memmap['Endereço']) + ',' + 
                    memmap['Registrador'] + ',' + 
                    memmap['Range'] + ',' + 
                    memmap['Unidade'] + ',' + 
                    memmap['Tipo / Função'] + ',' + 
                    str(memmap['Valor']))
                  f.write('\n')
                  
                  print("=============================")

                  print('Memory Map number #{}: '.format(memmap['Endereço']))
                  print('\tRegistrador: {}'.format(memmap['Registrador']))
                  print('\tTipo / Função: {}'.format(memmap['Tipo / Função']))
                  print('\tRange: {}'.format(memmap['Range']))
                  print('\tUnidade: {}'.format(memmap['Unidade']))
                  print('\tValor: {}'.format(memmap['Valor']))

              print("=============================")

          f.close()
          print("MODBUS:: READ MEMORY MAP FINISHED!")

      else:
          print("MODBUS:: READ MEMORY MAP ERROR. End of execution.")
  else:
    print('Unable to read CSV file: [{}]. End of execution.'.format(csv_file))

if __name__ == "__main__":
  main()


