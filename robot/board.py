import time
import logging
import pigpio

from robot import led
from robot import buzzer
from robot import servo
from robot import motor
from robot.sensor import ultrasound
from robot import camera

from threading import Thread
from RPi import GPIO


logging.basicConfig(format='%(asctime)s %(levelname)s (%(process)d) %(filename)s %(funcName)s %(message)s')


class Board(Thread):

    """
        Thread controlling Robot actions
    """
        
    def __init__(self, waitTime = 0.05, *args, **kwargs):
        
        Thread.__init__(self, *args, **kwargs)

        self._gpio = pigpio.pi()
        GPIO.setmode(GPIO.BCM)
        
        self._run = True
    
        self._ledR = led.Led('R', self._gpio, 22, led.OFF)
        self._ledG = led.Led('G', self._gpio, 27, led.OFF)
        self._ledB = led.Led('B', self._gpio, 24, led.OFF)
        
        self._buzzer = buzzer.Buzzer('buzzer', self._gpio, 8, buzzer.OFF)
        
        self._ledServo = servo.Servo('ledServo', self._gpio, pin=23, frequency=50, initialValue=servo.Servo.angle2dc(105))

        self._camServoV =  servo.Servo('camServoV', self._gpio, pin=9, frequency=50, initialValue=servo.Servo.angle2dc(60))
        self._camServoH =  servo.Servo('camServoH', self._gpio, pin=11, frequency=50,
        initialValue=servo.Servo.angle2dc(105))

        self._rMotor = motor.Motor('rightMotor', self._gpio, pin=13, frequency=2000, pinIn1=19, pinIn2=26)
        self._lMotor = motor.Motor('leftMotor', self._gpio, pin=16, frequency=2000, pinIn1=20, pinIn2=21)

        self._camera = camera.Camera('camera')

        self._ultrasound = ultrasound.Ultrasound('ultrasound', GPIO, pinIn=0, pinOut=1)

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

    @property
    def camServoV(self):
        self._logger.info('Board')
        return self._camServoV

    @property
    def camServoH(self):
        self._logger.info('Board')
        return self._camServoH

    @property
    def camera(self):
        self._logger.info('Board')
        return self._camera

    @property
    def rMotor(self):
        self._logger.info('Board')
        return self._rMotor

    @property
    def lMotor(self):
        self._logger.info('Board')
        return self._lMotor

    @property
    def ultrasound(self):
        self._logger.info('Board')
        return self._ultrasound
    
    def _shutdownComponents(self):
        self._logger.info('Board')
        
        self._ledR.stop()
        self._ledG.stop()
        self._ledB.stop()
        
        self._buzzer.stop()
        
        self._ledServo.stop()

        self._camServoV.stop()
        self._camServoH.stop()

        self._rMotor.stop()
        self._lMotor.stop()

        self._camera.stop()

        self._ultrasound.stop()
        
        while   self._ledR.is_alive() or \
                self._ledG.is_alive() or \
                self._ledB.is_alive() or \
                self._buzzer.is_alive() or \
                self._ledServo.is_alive() or \
                self._camServoV.is_alive() or \
                self._camServoH.is_alive() or \
                self._rMotor.is_alive() or \
                self._lMotor.is_alive() or \
                self._camera.is_alive() or \
                self._ultrasound.is_alive():
            pass
        
        self._gpio.stop()


    def set(self):
        """
        ### if board must do something
           do it here ###
        """
        pass

        
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

        self._camServoV.start()
        self._camServoH.start()

        self._rMotor.start()
        self._lMotor.start()

        self._camera.start()

        self._ultrasound.start()


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

    
    def moveForward(self, minValue, maxValue, readValue, safeDistance=10):

        self._ledServo.rotate_to(105)
        readDistance = self._ultrasound.distance()
        if readDistance > safeDistance:
            self._rMotor.setRelativeSpeed(minValue, maxValue, readValue)
            self._lMotor.setRelativeSpeed(minValue, maxValue, readValue)
            self._rMotor.forward()
            self._lMotor.forward()

        else:
            self._buzzer.beep(2)


    def moveBackward(self, minValue, maxValue, readValue):
        self._buzzer.beep(3, waitTime=0.8)
        self._rMotor.setRelativeSpeed(minValue, maxValue, readValue*0.75)
        self._lMotor.setRelativeSpeed(minValue, maxValue, readValue*0.75)
        self._rMotor.backward()
        self._lMotor.backward()


    def spinRight(self, minValue, maxValue, readValue):
        self._rMotor.setRelativeSpeed(minValue, maxValue, readValue) 
        self._lMotor.setRelativeSpeed(minValue, maxValue, readValue) 
        self._rMotor.backward() 
        self._lMotor.forward() 


    def spinLeft(self, minValue, maxValue, readValue):
        self._rMotor.setRelativeSpeed(minValue, maxValue, readValue) 
        self._lMotor.setRelativeSpeed(minValue, maxValue, readValue) 
        self._rMotor.forward() 
        self._lMotor.backward() 


    def halt(self):
        self._buzzer.off()
        self._rMotor.halt()
        self._lMotor.halt()

    
    def turnRight(self, minValue, maxValue, readValue):
        self._rMotor.speedRate = 0.25
        self._lMotor.speedRate = 1.0


    def turnLeft(self, minValue, maxValue, readValue):
        self._rMotor.speedRate = 1.0
        self._lMotor.speedRate = 0.25


    def center(self):
        self._rMotor.speedRate = 1.0
        self._lMotor.speedRate = 1.0


    def toggleLed(self, led):
        if led == 'R':
            self._ledR.toggle()
        elif led == 'G':
            self._ledG.toggle()
        elif led == 'B':
            self._ledB.toggle()


    def turnBuzzerOn(self):
        self._buzzer.on()
   

    def turnBuzzerOff(self):
        self._buzzer.off()


    def rotateLedClockwise(self):
        self._ledServo.rotate_clockwise()


    def haltLed(self):
        self._ledServo.halt()


    def rotateLedAntiClockwise(self):
        self._ledServo.rotate_anticlockwise()


    def moveCameraDown(self):
        self._camServoV.rotate_clockwise()


    def moveCameraUp(self):
        self._camServoV.rotate_anticlockwise()


    def haltCamera(self):
        self._camServoV.halt()
        self._camServoH.halt()


    def moveCameraRight(self):
        self._camServoH.rotate_clockwise()


    def moveCameraLeft(self):
        self._camServoH.rotate_anticlockwise()


