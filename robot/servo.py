import time
import logging

from threading import Thread

from robot.component import PWMComponent


logging.basicConfig(format='%(asctime)s %(levelname)s (%(process)d) %(filename)s %(funcName)s %(message)s')

MINDUTYCYCLE=2.5
MAXDUTYCYCLE=12.5
FREQUENCY=100
STEP=0.1


class Servo(PWMComponent, Thread):
    
    """
        Servo component
    """
    
    def __init__(self, label, gpio, pin, frequency=FREQUENCY, minDC=MINDUTYCYCLE, maxDC=MAXDUTYCYCLE, step=STEP, initialValue=None, waitTime = 0.05, *args, **kwargs):
        
        PWMComponent.__init__(self, label, gpio, pin, frequency, initialValue)
        
        Thread.__init__(self, *args, **kwargs)

        self._minDC = minDC
        self._maxDC = maxDC

        self._sign = 0
        self._step = step

        self._run = True

        self._waitTime = waitTime
        
        self._logger = logging.getLogger(self._label)
        self._logger.setLevel(logging.DEBUG)
                
        self._logger.info(self._label + ' started')

    
    @property
    def minDC(self):
        return self._minDC


    @property
    def maxDC(self):
        return self._maxDC


    @PWMComponent.state.setter
    def state(self, value):
        if value >= self._minDC and value <= self._maxDC:
            self._value = value
    
    @staticmethod
    def angle2dc(angle, minDC=MINDUTYCYCLE, maxDC=MAXDUTYCYCLE):
        return minDC + (maxDC-minDC)*angle/180

        
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


    def set(self):
        if self._sign > 0:
            if self._state + self._step <= self._maxDC:
                self._state += self._step
            else:
                self._state = self._maxDC

        elif self._sign < 0:
            if self._state - self._step >= self._minDC:
                self._state -= self._step
            else:
                self._state = self._minDC
                
        PWMComponent.set(self)


    def rotate_to(self, angle):
        self._logger.info(self._label)
        self.state = self.angle2dc(angle, minDC=self._minDC, maxDC=self._maxDC)


    def rotate_clockwise(self, step=None):
        self._logger.info(self._label)
        if step:
            self._step = step
        self._sign = -1


    def rotate_anticlockwise(self, step=None):
        self._logger.info(self._label)
        if step:
            self._step = step
        self._sign = 1


    def halt(self):
        self._logger.info(self._label)
        self._sign = 0
        self._pwm.ChangeDutyCycle(0)
