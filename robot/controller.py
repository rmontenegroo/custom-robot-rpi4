from pyPS4Controller.controller import Controller

from robot.board import Board
    
class RobotController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self._board = Board()
        self._board.start()


    def on_x_press(self):
        Controller.on_x_press(self)
        self._board._ledB.toggle()

    def on_x_release(self):
        Controller.on_x_release(self)


    def on_circle_press(self):
        Controller.on_circle_press(self)
        self._board._ledR.toggle()

    def on_circle_release(self):
        Controller.on_circle_release(self)


    def on_triangle_press(self):
        Controller.on_triangle_press(self)
        self._board._ledG.toggle()

    def on_triangle_release(self):
        Controller.on_triangle_release(self)


    def on_square_press(self):
        Controller.on_square_press(self)
        self._board._buzzer.on()

    def on_square_release(self):
        Controller.on_square_release(self)
        self._board._buzzer.off()

    
    def on_R1_press(self):
        Controller.on_R1_press(self)
        self._board._ledServo.rotate_clockwise()

    def on_R1_release(self):
        Controller.on_R1_release(self)
        self._board._ledServo.halt()


    def on_L1_press(self):
        Controller.on_L1_press(self)
        self._board._ledServo.rotate_anticlockwise()

    def on_L1_release(self):
        Controller.on_L1_release(self)
        self._board._ledServo.halt()


    def on_up_arrow_press(self):
        Controller.on_up_arrow_press(self)
        self._board._camServoV.rotate_clockwise()

    def on_down_arrow_press(self):
        Controller.on_down_arrow_press(self)
        self._board._camServoV.rotate_anticlockwise()

    def on_up_down_arrow_release(self):
        Controller.on_up_down_arrow_release(self)
        self._board._camServoV.halt()


    def on_right_arrow_press(self):
        Controller.on_right_arrow_press(self)
        self._board._camServoH.rotate_clockwise()

    def on_left_arrow_press(self):
        Controller.on_left_arrow_press(self)
        self._board._camServoH.rotate_anticlockwise()

    def on_left_right_arrow_release(self):
        Controller.on_left_right_arrow_release(self)
        self._board._camServoH.halt()


    def on_L3_up(self, value):
        Controller.on_L3_up(self, value)
        self._board._rMotor.forward()
        self._board._lMotor.forward()

    def on_L3_down(self, value):
        Controller.on_L3_down(self, value)
        self._board._rMotor.backward()
        self._board._lMotor.backward()

    def on_L3_y_at_rest(self):
        Controller.on_L3_y_at_rest(self)
        self._board.rMotor.halt()
        self._board.lMotor.halt()


