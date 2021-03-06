# cw.py
# Puts a LoRaMOTE into CW mode
#  Sending a series of Morse Vs
#  dit dit dit daaaaah   dit dit dit daaaaaah ...

import serial
import time

SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 115200

class LoraException(Exception):
  pass

class LoRaSerial(object):
    def __init__(self,freq=909000000):
        '''
            configures serial connection
        '''
        self._ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

        # timeout block read
        self._ser.timeout = 2

        # disable software flow control
        self._ser.xonxoff = False

        # disable hardware (RTS/CTS) flow control
        self._ser.rtscts = False

        # disable hardware (DSR/DTR) flow control
        self._ser.dsrdtr = False

        # timeout for write
        self._ser.writeTimeout = 0

        self.read()

        self.write_radio_config('mod lora')
        self.write_radio_config('pwr 20')
        self.write_radio_config('sf sf7')
        self.write_radio_config('afcbw 125')
        self.write_radio_config('fdev 5000')
        self.write_radio_config('prlen 8')
        self.write_radio_config('crc on')
        self.write_radio_config('cr 4/5')
        self.write_radio_config('wdt 0')
        self.write_radio_config('sync 12')
        self.write_radio_config('bw 125')
        self.write_radio_config('freq %d'%freq)
        self.write('mac pause')

    def read(self):
        '''
            reads serial input
        '''
        r = self._ser.readline().strip()
        #print "READ: ",r
        return r

    def write(self, str):
        '''
            writes out string to serial connection, returns response
        '''
        self._ser.write(str + '\r\n')
        #print "WROTE: ",str
        return self.read()
    
    def write_radio_config(self, config_str):
        '''
            writes out a radio config command
        '''
        response = self.write('radio set ' + config_str)
        if not response in ['k','ok']:
          raise LoraException("Error: Unexpected response: '%s'"%response)
        
    def send_message(self, str):
        '''
            sends a message to other LoRa devices
        '''
        self.write('radio tx ' + str.encode('hex'))
        message = ''
        while message == '':
          message = self.read()

    def get_snr(self):
      try:
        return int(self.write('radio get snr'))
      except:
        return 0

    def receive_message(self, wait=False, encoding='binary', timeout=0):
        '''
            waits for a message
        '''
        self.write('radio rx %d'%timeout)

        message = self.read()
        if wait:
            while message == '':
                message = self.read()

        if '_err' in message:
          return ''

        message = message.replace('radio_rx  ', '')
        if not encoding == 'hex':
          message = message.decode('hex')

        return message

