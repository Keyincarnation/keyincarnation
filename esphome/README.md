This is the esphome configuration used for basic power switching and controls for the piano.

## Requirements
* A running Home Assistant instance on your network.
* The ESPHome addon installed in Home Assistant.
* A Sonoff Dual R2 or similar.
* Headers soldered
* A secrets.yaml file that includes the wifi ssid and password.

## Connections
### Power
* The speaker amplifier on the primary connection. (GPIO05)
* The rest (Raspberry, headerphone amp) on the secondary. (GPIO12)
### Sensors
I used external Pullup resistors of 4.7 kOhm as the internal pullups seem to give me trouble earlier. Connect the pullup resistor between the GPIO pins and the 3.3V pin.
* The keylid reed sensor on the RX pin (GPIO01)
* The speaker on/of switch on the TX pin (GPIO03)
### IR transmitter
I used two small, low power IR Leds in serial to control the led candles.
* IR Leds on GPIO09

## Notes
I avoided using GPIO04 as it will set the Sonoff to flash mode when connected during boot. 
