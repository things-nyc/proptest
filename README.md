### Installation ###

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

