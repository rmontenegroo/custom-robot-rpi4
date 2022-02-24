from pyPS4Controller.controller import Controller

from robot.board import Board
    
class RobotController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

        self._board = Board()

        self._board.start()


    def on_x_press(self):
        Controller.on_x_press(self)
        self._board._ledB.on()


    def on_x_release(self):
        Controller.on_x_release(self)
        self._board._ledB.off()

