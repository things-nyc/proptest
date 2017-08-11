#### Abstract ####

proptest is a python script for controlling a Microchip RN2903 "LoRaMOTE" for use in indoor propagation experiments.
These experiments are for studying the ability of a 900MHz LoRa signal to reach different parts of a building.
It uses simplex LoRa (not LoRaWAN/TTN) and does not channel hop, and therefore we operate under Part 97 rules and
require an amateur radio license. One of the stated purposes of the amateur radio service is "advancing the radio art",
which in this case means feeding back knowledge to The Things Network about indoor propagation.

We use 6dBi sleeve dipole antennas (stock with the LoRaMOTES) and 20dBm (100mW) transmit power. See source for modulation details. Results from data taken with this setup can be extrapolated to other more limited situations (smaller antennas, less tx power, etc.). Higher power studies could also be interesting and possible with amateur radio license (permitting up to 10W on 33cm and unlimited antenna gain, up to human exposure considerations).

#### Requirements ####

 - Python 2.7
 - pyserial: `pip install pyserial`
 - Microchip LoRaMOTE (or other board providing a usb-serial connection to an RN2903)
 - USB mini-B cable
 - Amateur radio license

#### Usage ####

 1. Plug in LoRaMOTE to laptop.
 2. Run `python -freq 909000000 --call W1AW --loc R302`,
    where you replace `W1AW` with your amateur callsign,
    and specify the room number you are in using the `loc` field.
 3. You should now see a console printing colored messages,
    yellow indicating your transmissions,
    green indicating reception from other nodes.
 4. To exit, press Ctrl-C.
 5. When you move to a new room, or out into a common space,
    you can issue the python command again with the new location.

#### Known Issues ####

 1. **no logging to disk**: we need some sort of logging capability, perhaps using the
    callsign, location, frequency, and datetime as part of the filename.
 2. **errors during configuration**: can be resolved by retrying multiple times and/or
    unplugging/replugging the LoRaMOTE. Would be good to resolve this.
 3. **synchronization of transmissions**: although there is randomness in timing of transmissions,
    the current algorithm may lead collisions immediately after receiving a packet.
    This could be resolved by enforcing a pre-computed random interval between transmissions,
    by issuing a new `radio_rx` request with a timeout corresponding to the remaining
    time in the interval, rather than just immediately transmitting as is the current algorithm.
 4. **frequency/spreading factor**: more of an experiment design issue: 
    currently we use SF7 and a fixed frequency. Choice of frequency and SF will effect range,
    due to QRM and differing coding gains. However, SF7 has been chosen here to minimize collisions,
    and because it is the reasonable default for TTN applications if ADR is not implemented.

