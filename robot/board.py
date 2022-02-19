import RPi.GPIO as gpio
import time
import logging

from robot import led
from robot import buzzer
from robot import servo

from threading import Thread


logging.basicConfig(format='%(asctime)s %(levelname)s (%(process)d) %(filename)s %(funcName)s %(message)s')


class Board(Thread):

	"""
		Thread controlling Robot actions
	"""
		
	def __init__(self, waitTime = 0.05, *args, **kwargs):
		
		Thread.__init__(self, *args, **kwargs)

		self._gpio = gpio
		
		self._gpio.setmode(self._gpio.BCM)

		self._run = True
	
		self._ledR = led.Led('R', self._gpio, 22, led.OFF)
		self._ledG = led.Led('G', self._gpio, 27, led.OFF)
		self._ledB = led.Led('B', self._gpio, 24, led.OFF)
		
		self._buzzer = buzzer.Buzzer('buzzer', self._gpio, 8, buzzer.OFF)
		
		self._ledServo = servo.Servo('ledServo', self._gpio, pin=23, freq=50, angle=90)

		self._waitTime = waitTime
			
		self._logger = logging.getLogger('board')
		self._logger.setLevel(logging.DEBUG)
				
		self._logger.info('Board')

		
	@property
	def gpio(self):
		self._logger.info('Board')
		return self._gpio
		
	@property
	def buzzer(self):
		return self._buzzer
		
	@property
	def ledR(self):
		self._logger.info('Board')
		return self._ledR
		
	@property
	def ledG(self):
		self._logger.info('Board')
		return self._ledG
	
	@property
	def ledB(self):
		self._logger.info('Board')
		return self._ledB
		
	@property
	def ledServo(self):
		self._logger.info('Board')
		return self._ledServo
	
	def set(self):
		pass
		
	def _shutdownComponents(self):
		self._logger.info('Board')
		
		self._ledR.stop()
		self._ledG.stop()
		self._ledB.stop()
		
		self._buzzer.stop()
		
		self._ledServo.stop()
		
		while 	self._ledR.is_alive() or \
				self._ledG.is_alive() or \
				self._ledB.is_alive() or \
				self._buzzer.is_alive() or \
				self._ledServo.is_alive():
			pass
		
		self._gpio.cleanup()

		
	def stop(self):
		self._logger.info('Board')

		self._run = False


	def _initComponents(self):
		self._logger.info('Board')
		
		self._buzzer.start()
						
		self._ledR.start()
		self._ledG.start()
		self._ledB.start()
		
		self._ledServo.start()

	
	def run(self):
		self._logger.info('Board')
				
		try:
			self._initComponents()
			
			self._buzzer.beep(2)
			
			while self._run:
										
				self.set()
							
				time.sleep(self._waitTime)
				
		except Exception as e :
			self._logger.info('Board exception')
			self._logger.error(str(e))
			raise e
			
		finally:
			self._logger.info('Board finally')
			self._buzzer.beep(3)
			self._shutdownComponents()
