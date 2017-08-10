'''
   propagation measurement program

   location 502B   [exactly 12 bytes]
   callsign WA2ABC [exactly 12 bytes]

'''

from lora_serial import LoRaSerial
import time
import sys
import json
import re
import string
import argparse
import random

parser = argparse.ArgumentParser(description='Test 33cm propagation.')
parser.add_argument('--call',required=True,help='your amateur radio callsign')
parser.add_argument('--freq',help='specify frequency in Hz',required=True)
args = parser.parse_args()

MIN_TX_IVAL = 5
MAX_TX_IVAL = 10
t_next_tx = time.time()

callsign = args.call.upper()
location = 'init'

freq = int(args.freq)
print "*** Starting LoRa Transceiver on Frequency %d Hz"%freq
lora = LoRaSerial(freq)

class termcol:
  KNRM = '\033[0m'
  KBLD = '\033[1m'
  KRED = '\033[31m'
  KGRN = '\033[32m'
  KYEL = '\033[33m'
  KGRE = '\033[37m'

replchars = re.compile(re.compile('([^' + re.escape(string.printable) + '])'))
def replchars_to_hex(match):
  return r'\x{0:02x}'.format(ord(match.group()))

while True:
  now = time.time()
  if now > t_next_tx:
    t_next_tx = now + random.random()*(MAX_TX_IVAL-MIN_TX_IVAL) + MIN_TX_IVAL
    tx_text = '%-12s de %12s'%(location,callsign)
    tx_hex = ''.join('{:02x}'.format(ord(c)) for c in tx_text)
    print termcol.KYEL+'%s: %-24s'%(time.strftime("%Y%m%d:%H%M%S"),tx_text)+termcol.KNRM
    lora.send_message(tx_hex)

  rx_msg = lora.receive_message(wait=False,encoding='hex')
  if len(rx_msg) > 0:
    snr = lora.get_snr()
    dangerous_ascii = rx_msg.decode('hex')
    rx_text = replchars.sub(replchars_to_hex, dangerous_ascii)
    print termcol.KGRN+'%s: %-24s'%(time.strftime("%Y%m%d:%H%M%S"),tx_text)
    print '%s: %-24s:  '%(time.strftime("%Y%m%d:%H%M%S"),rx_text),
    print 'SNR ' + str(snr)+termcol.KNRM


