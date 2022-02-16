import RPi.GPIO as GPIO

ON = GPIO.HIGH
OFF = GPIO.LOW

class Led(object):
	
	"""
		Represents info about Leds on board
	"""
	
	def __init__(self, label, pin, initialState=ON):
		self._label = label
		self._state = initialState
		self._pin = pin
								
	def set(self):
		GPIO.setup(self._pin, GPIO.OUT)
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
