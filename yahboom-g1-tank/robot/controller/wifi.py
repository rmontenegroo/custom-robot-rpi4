import socket
import logging

from robot.board import Board


logging.basicConfig(format='%(asctime)s %(levelname)s (%(process)d) %(filename)s %(funcName)s %(message)s')

    
class WiFiController(object):

    def __init__(self, port=5005, **kwargs):

        self._label = 'wifi.controller'

        self._run = True

        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self._logger = logging.getLogger(self._label)
        self._logger.setLevel(logging.DEBUG)

        self._robot = Board()

        self._reverseAction = None
        self._action = None

        self._generalActions = {
            'device1on': lambda: self._changeActionsSet(self._ledServoActions),
            'device1off': lambda: self._changeActionsSet(self._generalActions),
            'device2on': lambda: self._changeActionsSet(self._cameraServoActions),
            'device2off': lambda: self._changeActionsSet(self._generalActions),

            'device4on': lambda: self._robot.lightsOn(),
            'device4off': lambda: self._robot.lightsOff(),

            'action 1': lambda: self._robot.turnBuzzerOn(),
            'action2': lambda: self._robot.streamer.snapshot(),

            'forward': lambda: self._robot.moveForward(0, 100, 100),
            'backward': lambda: self._robot.moveBackward(0, 100, 100),
            'right': lambda: self._robot.spinRight(0, 100, 50),
            'left': lambda: self._robot.spinLeft(0, 100, 50),

            'stop': lambda: self._reverseAction(),
        }

        self._ledServoActions = {
            'device1on': lambda: self._changeActionsSet(self._ledServoActions),
            'device1off': lambda: self._changeActionsSet(self._generalActions),
            'device2on': lambda: self._changeActionsSet(self._cameraServoActions),
            'device2off': lambda: self._changeActionsSet(self._generalActions),

            'right': lambda: self._robot.rotateLedClockwise(),
            'left': lambda: self._robot.rotateLedAntiClockwise(),

            'stop': lambda: self._robot.haltLed(),
        }

        self._cameraServoActions = {
            'device1on': lambda: self._changeActionsSet(self._ledServoActions),
            'device1off': lambda: self._changeActionsSet(self._generalActions),
            'device2on': lambda: self._changeActionsSet(self._cameraServoActions),
            'device2off': lambda: self._changeActionsSet(self._generalActions),

            'forward': lambda: self._robot.moveCameraUp(),
            'backward': lambda: self._robot.moveCameraDown(),
            'right': lambda: self._robot.moveCameraRight(),
            'left': lambda: self._robot.moveCameraLeft(),

            'stop': lambda: self._robot.haltCamera(),
        }

        self._reverseActions = {
            'action 1': lambda: self._robot.turnBuzzerOff(),
            'forward': lambda: self._robot.halt(),
            'backward': lambda: self._robot.halt(),
            'right': lambda: self._robot.halt(),
            'left': lambda: self._robot.halt(),
        }

        self._actionsSet = self._generalActions

        self._logger.info(self._label + ' started')


    def shutdown(self):
        self._logger.info(self._label)
        self._run = False


    def listen(self):
        self.run()


    def _changeActionsSet(self, aSet):
        self._actionsSet = aSet


    def run(self):        

        def defaultAction():
            print('Action not mapped')

        def defaultReverseAction():
            print('Reverse action not mapped')
            
        self._robot.start()

        try:

            self._socket.bind(("", self._port))

            while self._run:

                cmd, addr = self._socket.recvfrom(1024)
                self._logger.info(f'cmd: {cmd}  addr: {addr}')

                cmd = cmd.decode()
                self._action = self._actionsSet.get(cmd, defaultAction)
                self._action()

                self._reverseAction = self._reverseActions.get(cmd, defaultReverseAction)

        except Exception as e :
            self._logger.info(self._label + ' exception')
            raise e

        finally:
            self.close()


    def close(self):
        self._logger.info(self._label)
        self._socket.close()
        self._robot.stop()



