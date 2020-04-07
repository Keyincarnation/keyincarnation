#!/usr/bin/python3

import time
import rtmidi

import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017

class SelectSwitch:

  def __init__(self, mcp):
    self.pins = []
    for i in range(12):
      self.pins.insert(i , mcp.get_pin(i))
      self.pins[i].direction = digitalio.Direction.INPUT
      self.pins[i].pull = digitalio.Pull.UP
    self.value = self.get_value()

  def get_value(self):
    scanning = True
    current_pin = 0
    while scanning:
      print("Scanning pin " + str(current_pin))
      if self.pins[current_pin].value == False:
        time.sleep(0.1)
        if self.pins[current_pin].value == False:
          selected = current_pin
          print("selected: " + str(selected))
          scanning = False
        # if current_pin < 12:
      current_pin = current_pin + 1
      if current_pin == 12:
        current_pin = 0
    return selected

  def update(self):
    # changed = self.pins[self.value].value == self.value
    changed = self.pins[self.value].value != False
    if changed:
      self.value = self.get_value()
    return changed

class BinarySwitch:

  def __init__(self, mcp, pin):
    self.switch = mcp.get_pin(pin)
    self.switch.direction = digitalio.Direction.INPUT
    self.switch.pull = digitalio.Pull.UP
    self.value = self.switch.value
  
  def update(self):
    changed = self.value != self.switch.value
    if changed:
      self.value = self.switch.value
    return changed


class MidiPort:

  def __init__(self):
    self.midiout = rtmidi.MidiOut()
    self.midiout.open_virtual_port("PianoControl")

  def program_change(self,program):
    midi_cmd = [0xC0, program]
    self.midiout.send_message(midi_cmd)

class PianoControl:

  def __init__(self):
    self.i2c = busio.I2C(board.SCL, board.SDA)
    self.mcp = MCP23017(self.i2c)
    self.instrument_switch = SelectSwitch(self.mcp)
    self.effect1_switch = BinarySwitch(self.mcp,13)
    self.effect2_switch = BinarySwitch(self.mcp,14)
    self.headphone_switch = BinarySwitch(self.mcp,15)
    self.midi = MidiPort()
    self.instrument = self.instrument_switch.value
    # if self.headphone_switch.value:
    #  self.instrument = self.instrument + 12

  def check_instrument_change(self):
    instrument_changed = self.instrument_switch.update()
    headphone_changed = self.headphone_switch.update()
    changed = instrument_changed or headphone_changed 
    if changed:
      instrument = self.instrument_switch.value
      # if self.headphone_switch.value:
        # instrument = instrument + 12
      self.instrument = instrument
      print(instrument)
    return changed
   
## Main routine

piano = PianoControl()

while True:
  instrument_changed = piano.check_instrument_change() 
  if instrument_changed:
    piano.midi.program_change(piano.instrument)
    time.sleep(0.2)
  else:
    time.sleep(0.4)
  
