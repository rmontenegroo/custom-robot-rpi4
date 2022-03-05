from pyPS4Controller.controller import Controller

from robot.board import Board
    
class RobotController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self._robot = Board()
        self._robot.start()


    def shutdown(self):
        self._robot.stop()

    ################ leds ################################

    def on_x_press(self):
        self._robot.toggleLed('B')

    def on_circle_press(self):
        self._robot.toggleLed('R')

    def on_triangle_press(self):
        self._robot.toggleLed('G')

    def on_R3_press(self):
        self._robot.toggleLights()

    ######################################################


    ################ buzzer ##############################

    def on_square_press(self):
        self._robot.turnBuzzerOn()

    def on_square_release(self):
        self._robot.turnBuzzerOff()

    ######################################################


    ##########  let/ultrasonic sensor servo ##############
    
    def on_R1_press(self):
        self._robot.rotateLedClockwise()

    def on_R1_release(self):
        self._robot.haltLed()

    def on_L1_press(self):
        self._robot.rotateLedAntiClockwise()

    def on_L1_release(self):
        self._robot.haltLed()

    ######################################################


    ################ camera servo ########################

    def on_up_arrow_press(self):
        self._robot.moveCameraUp()

    def on_down_arrow_press(self):
        self._robot.moveCameraDown()

    def on_up_down_arrow_release(self):
        self._robot.haltCamera()

    def on_right_arrow_press(self):
        self._robot.moveCameraRight()

    def on_left_arrow_press(self):
        self._robot.moveCameraLeft()

    def on_left_right_arrow_release(self):
        self._robot.haltCamera()

    ######################################################


    ################## motors ############################
    
    def on_L3_up(self, value):
        self._robot.moveForward(-32767, 0, value)

    def on_L3_down(self, value):
        self._robot.moveBackward(0, 32767, value)

    def on_R2_press(self, value):
        self._robot.spinRight(0, 100, 50)

    def on_R2_release(self):
        self._robot.halt()

    def on_L2_press(self, value):
        self._robot.spinLeft(0, 100, 50)

    def on_L2_release(self):
        self._robot.halt()

    def on_L3_y_at_rest(self):
        self._robot.halt()

    def on_R3_right(self, value):
        self._robot.turnRight(0, 32767, value)

    def on_R3_left(self, value):
        self._robot.turnLeft(0, 32767, value)

    def on_R3_x_at_rest(self):
        self._robot.center()

    ######################################################


    ################## camera ############################

    def on_share_press(self):
        self._robot.camera.snapshot()

    ######################################################


