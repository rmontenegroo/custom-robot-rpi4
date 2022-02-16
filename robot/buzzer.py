import RPi.GPIO as GPIO

ON = GPIO.LOW
OFF = GPIO.HIGH

class Buzzer(object):
	
	"""
		Represents info about buzzer on board
	"""
	
	def __init__(self, label, pin, initialState=OFF):
		self._label = label
		self._state = initialState
		self._pin = pin
		self._initialState = initialState
								
	def set(self):
		GPIO.setup(self._pin, GPIO.OUT, initial=OFF)
		GPIO.output(self._pin, self._state)
				
	def on(self):
		self._state = ON
		
	def off(self):
		self._state = OFF
				
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
