import RPi.GPIO as GPIO

import time

ON = GPIO.LOW
OFF = GPIO.HIGH

class Buzzer(object):
	
	"""
		Represents info about buzzer on board
	"""
	
	def __init__(self, label, pin, gpio, initialState=OFF):
		self._label = label
		self._state = initialState
		self._pin = pin
		self._gpio = gpio
		self._initialState = initialState
		
		self._gpio.setup(self._pin, self._gpio.OUT, initial=OFF)
								
	def set(self):
		self._gpio.output(self._pin, self._state)
				
	def on(self):
		self._state = ON
		
	def off(self):
		self._state = OFF
				
	def beep(self):
		self._state = ON
		time.sleep(0.2)
		self._state = OFF
		time.sleep(0.2)
		self._state = ON
		time.sleep(0.2)
		self._state = OFF
				
	@property
	def gpio(self):
		return self._gpio
				
	@property
	def pin(self):
		return self._pin
		
	@property
	def state(self):
		return self._state
		
	@state.setter
	def state(self, state):
		self._state = state
		
	@property
	def label(self):
		return self._label
		
	def toggle(self):
		if self._state == ON:
			self._state = OFF
		else:
			self._state = ON
