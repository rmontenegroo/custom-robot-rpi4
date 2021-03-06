import time
import logging
import pigpio
import yaml

from robot import led
from robot import buzzer
from robot import servo
from robot import motor
from robot.sensor import ultrasound
from robot import streamer

from threading import Thread
from RPi import GPIO


logging.basicConfig(format='%(asctime)s %(levelname)s (%(process)d) %(filename)s %(funcName)s %(message)s')

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

class Board(Thread):

    """
        Thread controlling Robot actions
    """
        
    def __init__(self, safeForwardDistance = config['board']['safeForwardDistance'], waitTime=config['board']['waitTime'], *args, **kwargs):
        
        Thread.__init__(self, *args, **kwargs)

        self._gpio = pigpio.pi()
        GPIO.setmode(GPIO.BCM)

        self._safeForwardDistance = safeForwardDistance
        
        self._run = True
    
        self._ledR = led.Led('R', self._gpio, config['leds']['red']['pin'], led.OFF)
        self._ledG = led.Led('G', self._gpio, config['leds']['green']['pin'], led.OFF)
        self._ledB = led.Led('B', self._gpio, config['leds']['blue']['pin'], led.OFF)
        
        self._buzzer = buzzer.Buzzer('buzzer', self._gpio, config['buzzer']['pin'], buzzer.OFF)
        
        self._ledServo = servo.Servo(
            'ledServo', 
            self._gpio, 
            pin=config['leds']['servo']['pin'], 
            frequency=config['leds']['servo']['frequency'], 
            initialValue=servo.Servo.angle2dc(config['leds']['servo']['initialValue'])
        )

        self._camServoV =  servo.Servo(
            'camServoV', 
            self._gpio, 
            pin=config['camera']['servoV']['pin'],
            frequency=config['camera']['servoV']['frequency'],
            initialValue=servo.Servo.angle2dc(config['camera']['servoV']['initialValue'])
        )

        self._camServoH =  servo.Servo(
            'camServoH', 
            self._gpio, 
            pin=config['camera']['servoH']['pin'],
            frequency=config['camera']['servoH']['frequency'],
            initialValue=servo.Servo.angle2dc(config['camera']['servoH']['initialValue'])
        )

        self._rMotor = motor.Motor(
            'rightMotor', 
            self._gpio, 
            pin=config['motors']['right']['pin'], 
            frequency=config['motors']['right']['frequency'], 
            pinIn1=config['motors']['right']['pinIn1'], 
            pinIn2=config['motors']['right']['pinIn2']
        )

        self._lMotor = motor.Motor(
            'leftMotor', 
            self._gpio, 
            pin=config['motors']['left']['pin'], 
            frequency=config['motors']['left']['frequency'], 
            pinIn1=config['motors']['left']['pinIn1'], 
            pinIn2=config['motors']['left']['pinIn2']
        )

        self._ultrasound = ultrasound.Ultrasound(
            'ultrasound', 
            GPIO, 
            pinIn=config['sensors']['ultrasound']['pinIn'], 
            pinOut=config['sensors']['ultrasound']['pinOut'], 
            emergencyStopCallable=self.emergencyHalt, emergencyStopDistanceThreshold=self.safeForwardDistance
        )

        self._streamer = streamer.Streamer(
            deviceName=config['camera']['deviceName'], 
            fps=config['camera']['fps'], 
            webServerPort=config['camera']['webServerPort'], 
            flipV=config['camera']['flipV'], 
            flipH=config['camera']['flipH'],
            waitTime=config['camera']['waitTime'],
        )

        self._waitTime = waitTime
            
        self._logger = logging.getLogger('board')
        self._logger.setLevel(logging.DEBUG)
                
        self._logger.info('Board')


    @property
    def safeForwardDistance(self):
        return self._safeForwardDistance

    @safeForwardDistance.setter        
    def safeForwardDistance(self, value):
        self._safeForwardDistance = value


    @property
    def streamer(self):
        self._logger.info('Board')
        return self._streamer

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

        self._ultrasound.stop()

        self._streamer.stop()
        
        
        while   self._ledR.is_alive() or \
                self._ledG.is_alive() or \
                self._ledB.is_alive() or \
                self._buzzer.is_alive() or \
                self._ledServo.is_alive() or \
                self._camServoV.is_alive() or \
                self._camServoH.is_alive() or \
                self._rMotor.is_alive() or \
                self._lMotor.is_alive() or \
                self._streamer.is_alive() or \
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

        self._ultrasound.start()

        self._streamer.start()


    def run(self):
        self._logger.info('Board')
                
        try:
            self._initComponents()
            
            self._buzzer.beep(2, waitTime=0.1)
            self._ledR.blink(2, waitTime=0.1)
            self._ledG.blink(2, waitTime=0.1)
            self._ledB.blink(2, waitTime=0.1)
            
            while self._run:
                                        
                self.set()
                            
                time.sleep(self._waitTime)
                
        except Exception as e :
            self._logger.info('Board exception')
            self._logger.error(str(e))
            raise e
            
        finally:
            self._logger.info('Board finally')
            self._buzzer.beep(3, waitTime=0.1)
            self._ledR.blink(3, waitTime=0.1)
            self._ledG.blink(3, waitTime=0.1)
            self._ledB.blink(3, waitTime=0.1)
            self._shutdownComponents()

    
    def moveForward(self, minValue, maxValue, readValue):

        if self._ledServo.state != servo.Servo.angle2dc(105):
            self._ledServo.rotate_to(105)

        if self._ultrasound.distance() > self._safeForwardDistance:
            self._rMotor.setRelativeSpeed(minValue, maxValue, readValue)
            self._lMotor.setRelativeSpeed(minValue, maxValue, readValue)
            self._rMotor.forward()
            self._lMotor.forward()


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


    def emergencyHalt(self):
        if self._rMotor.state == (motor.HIGH, motor.LOW) \
            and self._lMotor.state == (motor.HIGH, motor.LOW):

            self._rMotor.halt()
            self._lMotor.halt()

    
    def turnRight(self, minValue, maxValue, readValue):
        self._rMotor.speedRate = 0.5
        self._lMotor.speedRate = 1.25


    def turnLeft(self, minValue, maxValue, readValue):
        self._rMotor.speedRate = 1.25
        self._lMotor.speedRate = 0.5


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


    def areAnyLightsOn(self):
        return self._ledR.state == led.ON or \
            self._ledG.state == led.ON or \
            self._ledB.state == led.ON

    
    def areAnyLightsOff(self):
        return self._ledR.state == led.OFF or \
            self._ledG.state == led.OFF or \
            self._ledB.state == led.OFF


    def areAllLightsOn(self):
        return self._ledR.state == led.ON and \
            self._ledG.state == led.ON and \
            self._ledB.state == led.ON

    
    def areAllLightsOff(self):
        return self._ledR.state == led.OFF and \
            self._ledG.state == led.OFF and \
            self._ledB.state == led.OFF


    def lightsOn(self):
        self._ledR.on()
        self._ledG.on()
        self._ledB.on()


    def lightsOff(self):
        self._ledR.off()
        self._ledG.off()
        self._ledB.off()


    def toggleLights(self):
        if self.areAnyLightsOff():
            self.lightsOn()
        elif self.areAnyLightsOn():
            self.lightsOff()

    
    def takeSnapshot(self):
        self._streamer.snapshot(overwrite=False)

