import RPi.GPIO as GPIO
import time
import logging

from threading import Thread

from robot.component import OnOffComponent


logging.basicConfig(format='%(asctime)s %(levelname)s (%(process)d) %(filename)s %(funcName)s %(message)s')

ON = GPIO.HIGH
OFF = GPIO.LOW


class Led(OnOffComponent, Thread):
	
	"""
		Led component
	"""
	
	def __init__(self, label, gpio, pin, initialState=None, waitTime = 0.05, *args, **kwargs):
		OnOffComponent.__init__(self, label, gpio, pin, ON, OFF, initialState)
		Thread.__init__(self, *args, **kwargs)

		self._run = True

		self._waitTime = waitTime
		
		self._logger = logging.getLogger(self._label)
		self._logger.setLevel(logging.DEBUG)
				
		self._logger.info(self._label + ' started')

		
	def stop(self):
		self._logger.info(self._label)
		self._run = False
	
	
	def run(self):
		self._logger.info(self._label)
				
		try:
			
			while self._run:
										
				self.set()
							
				time.sleep(self._waitTime)
				
		except Exception as e :
			self._logger.info(self._label + ' exception')
			raise e
			
		finally:
			self._logger.info(self._label + ' finally')
			self.off()
			self.set()	


