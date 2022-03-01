from pyPS4Controller.controller import Controller

from robot.board import Board
    
class RobotController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self._board = Board()
        self._board.start()

    ################ leds ################################

    def on_x_press(self):
        self._board.ledB.toggle()

    def on_x_release(self):
        Controller.on_x_release(self)

    def on_circle_press(self):
        self._board.ledR.toggle()

    def on_circle_release(self):
        Controller.on_circle_release(self)

    def on_triangle_press(self):
        self._board.ledG.toggle()

    def on_triangle_release(self):
        Controller.on_triangle_release(self)

    ######################################################


    ################ buzzer ##############################

    def on_square_press(self):
        self._board.buzzer.on()

    def on_square_release(self):
        self._board.buzzer.off()

    ######################################################


    ##########  let/ultrasonic sensor servo ##############
    
    def on_R1_press(self):
        self._board.ledServo.rotate_clockwise()

    def on_R1_release(self):
        self._board.ledServo.halt()

    def on_L1_press(self):
        self._board.ledServo.rotate_anticlockwise()

    def on_L1_release(self):
        self._board.ledServo.halt()

    ######################################################


    ################ camera servo ########################

    def on_up_arrow_press(self):
        self._board.camServoV.rotate_clockwise()

    def on_down_arrow_press(self):
        self._board.camServoV.rotate_anticlockwise()

    def on_up_down_arrow_release(self):
        self._board.camServoV.halt()

    def on_right_arrow_press(self):
        self._board.camServoH.rotate_clockwise()

    def on_left_arrow_press(self):
        self._board.camServoH.rotate_anticlockwise()

    def on_left_right_arrow_release(self):
        self._board.camServoH.halt()

    ######################################################


    ################## motors ############################
    
    def on_L3_up(self, value):
        self._board.rMotor.setRelativeSpeed(-32767, 0, value)
        self._board.lMotor.setRelativeSpeed(-32767, 0, value)
        self._board.rMotor.forward()
        self._board.lMotor.forward()

    def on_L3_down(self, value):
        self._board.buzzer.beep(3, waitTime=0.8)
        self._board.rMotor.setRelativeSpeed(0, 100, 25)
        self._board.rMotor.setRelativeSpeed(0, 100, 25)
        self._board.rMotor.backward()
        self._board.lMotor.backward()

    def on_R2_press(self, value):
        # self._board.rMotor.setRelativeSpeed(-32767, 0, value)
        self._board.rMotor.setRelativeSpeed(0, 100, 50)
        # self._board.lMotor.setRelativeSpeed(-32767, 0, value)
        self._board.lMotor.setRelativeSpeed(0, 100, 50)
        self._board.rMotor.backward()
        self._board.lMotor.forward()

    def on_R2_release(self):
        self._board.rMotor.halt()
        self._board.lMotor.halt()

    def on_L2_press(self, value):
        # self._board.rMotor.setRelativeSpeed(-32767, 0, value)
        self._board.rMotor.setRelativeSpeed(0, 100, 50)
        # self._board.lMotor.setRelativeSpeed(-32767, 0, value)
        self._board.lMotor.setRelativeSpeed(0, 100, 50)
        self._board.rMotor.forward()
        self._board.lMotor.backward()

    def on_L2_release(self):
        self._board.rMotor.halt()
        self._board.lMotor.halt()

    def on_L3_y_at_rest(self):
        self._board.buzzer.off()
        self._board.rMotor.halt()
        self._board.lMotor.halt()

    def on_R3_right(self, value):
        rate = abs(value/32767)*0.8
        self._board.rMotor.speedRate = 1.0 - rate
        self._board.lMotor.speedRate = rate
        print(self._board.lMotor.speed, self._board.rMotor.speed)

    def on_R3_left(self, value):
        rate = abs(value/32767)*0.8
        self._board.rMotor.speedRate = rate
        self._board.lMotor.speedRate = 1.0 - rate
        print(self._board.lMotor.speed, self._board.rMotor.speed)

    def on_R3_x_at_rest(self):
        self._board.rMotor.speedRate = 1.0
        self._board.lMotor.speedRate = 1.0

    ######################################################


    ################## camera ############################

    def on_share_press(self):
        self._board.camera.snapshot()

    ######################################################

