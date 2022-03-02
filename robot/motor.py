import time
import logging

from threading import Thread

from RPi import GPIO as gpio

from robot.component import PWMComponent


logging.basicConfig(format='%(asctime)s %(levelname)s (%(process)d) %(filename)s %(funcName)s %(message)s')

HIGH = gpio.HIGH
LOW = gpio.LOW
FREQUENCY = 2000
MINSPEED = 1
MAXSPEED = 100


class Motor(PWMComponent, Thread):
    
    """
        Motor component
    """

    def __init__(self, label, gpio, pin, pinIn1, pinIn2, frequency=FREQUENCY, minSpeed=MINSPEED, maxSpeed=MAXSPEED, \
        initialState=(LOW, LOW), waitTime = 0.05, *args, **kwargs):
        
        PWMComponent.__init__(self, label, gpio, pin, frequency, initialState = None)
        
        Thread.__init__(self, *args, **kwargs)

        self._pinIn1 = pinIn1
        self._pinIn2 = pinIn2

        self._initialState = initialState

        self._minSpeed = minSpeed
        self._maxSpeed = maxSpeed
        self._speed = self._minSpeed
        self._speedRate = 1

        self._run = True

        self._waitTime = waitTime

        self._state = (LOW, LOW)

        self._gpio.setup(self._pinIn1, gpio.OUT)
        self._gpio.setup(self._pinIn2, gpio.OUT)
        self._gpio.setup(self._pin, gpio.OUT)

        self._gpio.output(self._pinIn1, self._state[0])
        self._gpio.output(self._pinIn2, self._state[1])
        self._pwm.ChangeDutyCycle(self._speed)
        
        self._logger = logging.getLogger(self._label)
        self._logger.setLevel(logging.DEBUG)
                
        self._logger.info(self._label + ' started')


    @property
    def minSpeed(self):
        return self._minSpeed


    @property
    def maxSpeed(self):
        return self._maxSpeed


    def setRelativeSpeed(self, minValue, maxValue, relValue):
        self._logger.info(self._label)
        self.speed = self._minSpeed + abs((self._maxSpeed - self._minSpeed)*relValue/(maxValue - minValue))


    @property
    def speed(self):
        return self._speed


    @speed.setter
    def speed(self, value):
        if value >= self._minSpeed and value <= self._maxSpeed:
            self._speed = value

    @property
    def speedRate(self):
        return self._speedRate


    @speedRate.setter
    def speedRate(self, value):
        if value >= 0 and value <= 1:
            self._speedRate = value


    @PWMComponent.state.setter
    def state(self, value):
        if hasattr(value, '__iter__') and len(value) == 2:
            self._state = value


    @property
    def pinIn1(self):
        return self._pinIn1


    @property
    def pinIn2(self):
        return self._pinIn2


    def set(self):
        self._gpio.output(self._pinIn1, self._state[0])
        self._gpio.output(self._pinIn2, self._state[1])
        self._pwm.ChangeDutyCycle(self._speed*self._speedRate)


    def forward(self, speed=None):
        self._state = (HIGH, LOW)
        if speed:
            self.speed = speed
    

    def backward(self, speed=None):
        self._state = (LOW, HIGH)
        if speed:
            self.speed = speed


    def halt(self):
        self._state = (LOW, LOW)
        self._speed = self._minSpeed


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
            self.cleanup()


