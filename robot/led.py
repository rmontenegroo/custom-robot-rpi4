import RPi.GPIO as GPIO

from robot.component import OnOffComponent

ON = GPIO.HIGH
OFF = GPIO.LOW

class Led(OnOffComponent):
	
	"""
		Represents info about Leds on board
	"""
	
	def __init__(self, label, gpio, pin, initialState=None):
		OnOffComponent.__init__(self, label, gpio, pin, ON, OFF, initialState)
