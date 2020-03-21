import time
import rtmidi

import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017
i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c)
midiout = rtmidi.MidiOut()
midiout.open_virtual_port("PianoControl")
selectpins = []
selected = 0

def midi_send_program_change(program):
  midi_cmd = [0xC0, program]
  midiout.send_message(midi_cmd)


for i in range(12):
  selectpins.insert(i , mcp.get_pin(i))
  selectpins[i].direction = digitalio.Direction.INPUT
  selectpins[i].pull = digitalio.Pull.UP
  print("pin" + str(i) + ":" + str(selectpins[i].value))

while True:
  if selectpins[selected].value == False:
    time.sleep(0.5)
  else:
    scanning = True
    current_pin = 0
    while scanning:
      print("Scanning pin " + str(current_pin))
      if selectpins[current_pin].value == False:
        selected = current_pin
        print("selected: " + str(selected))
        scanning = False
      else:
        if current_pin < 12:
          current_pin += 1
        else:
          scanning = False
    
