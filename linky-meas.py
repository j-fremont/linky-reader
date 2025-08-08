import serial
from datetime import datetime, timedelta, time
import requests

def main():

  with serial.Serial(port='/dev/ttyS0', baudrate=1200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.SEVENBITS, timeout=1) as ser:

    base = None

    while True:
      
      iinst = 0
      nb_iinst = 0

      finish = datetime.now() + timedelta(seconds=60)

      while datetime.now() < finish:

        line = ser.readline().decode("utf-8")

        if line.startswith('IINST'):
          iinst = iinst + int(line.split(' ')[1])
          nb_iinst = nb_iinst + 1
        if line.startswith('BASE'):
          base = int(line.split(' ')[1])

      if datetime.now().hour==2 and datetime.now().minute==0:
        data="elec iinst=" + str(round(iinst/nb_iinst, 2)) + "\nbase=" + str(base)
      else:
        data="elec iinst=" + str(round(iinst/nb_iinst, 2))

      try:
        requests.post("http://192.168.1.10:8086/write?db=homedb&precision=m", data=data, headers={'Content-Type': 'application/octet-stream'})
      except requests.exceptions.RequestException as e:
        print(e)

if __name__ == '__main__':
  main()

