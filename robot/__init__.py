import logging

from robot import board
from pyPS4Controller.controller import Controller

logging.basicConfig(format='%(asctime)s %(levelname)s (%(process)d) %(filename)s %(funcName)s %(message)s')


class Robot(Controller):
	
	"""
		Joystick interface to control the robot
	"""
	
	def __init__(self, interface, connecting_using_ds4drv=False, *args, **kwargs):
		Controller.__init__(self, interface=interface, connecting_using_ds4drv=connecting_using_ds4drv, *args, **kwargs)
		self._board = board.Board()
		self._logger = logging.getLogger('controller')
		self._logger.setLevel(logging.DEBUG)
		
		if not self._board.is_alive():
			self._board.start()
				
	def on_triangle_press(self):
		self._logger.info('on_triangle_press called')
		self._board.ledG.toggle()
		
	def on_circle_press(self):
		self._logger.info('on_circle_press called')
		self._board.ledR.toggle()
		
	def on_x_press(self):
		self._logger.info('on_x_press called')
		self._board.ledB.toggle()
		
	def on_triangle_release(self):
		self._logger.info('on_triangle_press called')
		
	def on_circle_release(self):
		self._logger.info('on_circle_press called')
		
	def on_x_release(self):
		self._logger.info('on_x_release called')
		
	def on_square_press(self):
		self._logger.info('on_square_press called')
		self._board.buzzer.on()

	def on_square_release(self):
		self._logger.info('on_square_release called')
		self._board.buzzer.off()
		
	def shutdown(self):
		self._board.shutdown()



