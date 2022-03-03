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
        # self._robot.camServoV.rotate_clockwise()

    def on_down_arrow_press(self):
        self._robot.moveCameraDown()
        # self._robot.camServoV.rotate_anticlockwise()

    def on_up_down_arrow_release(self):
        self._robot.haltCamera()
        # self._robot.camServoV.halt()

    def on_right_arrow_press(self):
        self._robot.moveCameraRight()
        # self._robot.camServoH.rotate_clockwise()

    def on_left_arrow_press(self):
        self._robot.moveCameraLeft()
        # self._robot.camServoH.rotate_anticlockwise()

    def on_left_right_arrow_release(self):
        self._robot.haltCamera()
        # self._robot.camServoH.halt()

    ######################################################


    ################## motors ############################
    
    def on_L3_up(self, value):
        self._robot.moveForward(-32767, 0, value, safeDistance=10)

    def on_L3_down(self, value):
        self._robot.moveBackward(0, 32767, value)

    def on_R2_press(self, value):
        self._robot.spinRight(0, 100, 50)
        """
        self._robot.rMotor.setRelativeSpeed(0, 100, 50)
        self._robot.lMotor.setRelativeSpeed(0, 100, 50)
        self._robot.rMotor.backward()
        self._robot.lMotor.forward()
        """

    def on_R2_release(self):
        self._robot.halt()
        """
        self._robot.rMotor.halt()
        self._robot.lMotor.halt()
        """

    def on_L2_press(self, value):
        self._robot.spinLeft(0, 100, 50)
        """
        self._robot.rMotor.setRelativeSpeed(0, 100, 50)
        self._robot.lMotor.setRelativeSpeed(0, 100, 50)
        self._robot.rMotor.forward()
        self._robot.lMotor.backward()
        """

    def on_L2_release(self):
        self._robot.halt()
        """
        self._robot.rMotor.halt()
        self._robot.lMotor.halt()
        """

    def on_L3_y_at_rest(self):
        self._robot.halt()
        """
        self._robot.buzzer.off()
        self._robot.rMotor.halt()
        self._robot.lMotor.halt()
        """

    def on_R3_right(self, value):
        self._robot.turnRight(0, 32767, value)
        """
        rate = abs(value/32767)*0.8
        self._robot.rMotor.speedRate = 1.0 - rate
        self._robot.lMotor.speedRate = rate
        """

    def on_R3_left(self, value):
        self._robot.turnLeft(0, 32767, value)
        """
        rate = abs(value/32767)*0.8
        self._robot.rMotor.speedRate = rate
        self._robot.lMotor.speedRate = 1.0 - rate
        """

    def on_R3_x_at_rest(self):
        self._robot.center()
        """
        self._robot.rMotor.speedRate = 1.0
        self._robot.lMotor.speedRate = 1.0
        """

    ######################################################


    ################## camera ############################

    def on_share_press(self):
        self._robot.camera.snapshot()

    ######################################################


