# Pianod
A python deamon running on the Raspberry Pi to control extra features of the piano.

## Current features
* Connect to the I2C connected mcp210017 i/o expander chip.
* Read the instrument selector switch, a 12-way rotary select switch.
* Read basic on/off switches.
* Send Midi program change messages.

## Future features
* Send Midi Control messages.
* Provide Home Assistant integration.

## Requirments
* Raspbian
* Python 3
* Adafruit CircuitPython libraries and dependencies
* rtmidi and with python3 bindings

