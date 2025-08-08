import serial
import requests

base = None

def main():

  with serial.Serial(port='/dev/ttyS0', baudrate=1200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.SEVENBITS, timeout=1) as ser:

    while True:

      line = ser.readline().decode("utf-8")

      if line.startswith('BASE'):
        base = int(line.split(' ')[1])
        data="elec base=" + str(base)
        try:
          requests.post("http://192.168.1.10:8086/write?db=homedb&precision=m", data=data, headers={'Content-Type': 'application/octet-stream'})
        except requests.exceptions.RequestException as e:
          raise SystemExit(e)
        break

if __name__ == '__main__':
  main()

