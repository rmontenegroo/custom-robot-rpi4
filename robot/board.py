import RPi.GPIO as GPIO
import time
import logging

from robot import led
from robot import buzzer

from threading import Thread


logging.basicConfig(format='%(asctime)s %(levelname)s (%(process)d) %(filename)s %(funcName)s %(message)s')


class Board(Thread):

	"""
		Thread controlling Robot actions
	"""
		
	def __init__(self, waitTime = 0.05, *args, **kwargs):
		
		Thread.__init__(self, *args, **kwargs)

		self._run = True
	
		self._ledR = led.Led('R', 22, led.OFF)
		self._ledG = led.Led('G', 27, led.OFF)
		self._ledB = led.Led('B', 24, led.OFF)
		
		self._buzzer = buzzer.Buzzer('buzzer', 8, buzzer.OFF)

		self._waitTime = waitTime
			
		self._logger = logging.getLogger('robot')
		self._logger.setLevel(logging.DEBUG)
				
		self._logger.info('Robot started')
		
		
	@property
	def buzzer(self):
		return self._buzzer
		
	@property
	def ledR(self):
		return self._ledR
		
	@property
	def ledG(self):
		return self._ledG
	
	@property
	def ledB(self):
		return self._ledB


	def flush(self):
		
		GPIO.setmode(GPIO.BCM)
		
		self._ledR.set()
		self._ledG.set()
		self._ledB.set()
		
		self._buzzer.set()
		

	def shutdown(self):
		
		self._logger.info('Robot shutdown')
		self._run = False


	def beep(self, beeps=2):
		for i in range(beeps):
			self._buzzer.on()
			self.flush()
			time.sleep(0.1)
			self._buzzer.off()
			self.flush()
			time.sleep(0.2)


	def _cleanup(self):
		
		GPIO.setmode(GPIO.BCM)
		
		self._ledR.off()
		self._ledG.off()
		self._ledB.off()
		
		self._ledR.set()
		self._ledG.set()
		self._ledB.set()
		
		self.beep(3)
		self._buzzer.off()
		self._buzzer.set()
		
		GPIO.cleanup()

	
	def run(self):
				
		try:
			self.beep()
			
			while self._run:
										
				self.flush()
							
				time.sleep(self._waitTime)
				
		except Exception as e :
			self._logger.error(str(e))
			raise e
			
		finally:
			self._cleanup()

