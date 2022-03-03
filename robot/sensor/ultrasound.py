import time
import logging

from RPi import GPIO
from threading import Thread

from robot.component import NPinComponent


logging.basicConfig(format='%(asctime)s %(levelname)s (%(process)d) %(filename)s %(funcName)s %(message)s')


HIGH = GPIO.HIGH
LOW = GPIO.LOW


class Ultrasound(Thread):
    
    """
        Ultrasound component
    """

    def __init__(self, label, gpio, pinIn, pinOut, initialState = LOW, readInterval=0.000002, waitTime = 0.05, *args, **kwargs):

        self._gpio = gpio

        self._label = label

        self._pinIn = pinIn
        self._pinOut = pinOut
        self._initialState = initialState
        self._state = initialState

        self._gpio.setup(pinIn, GPIO.IN)
        self._gpio.setup(pinOut, GPIO.OUT)

        if self._initialState is not None:
            self._gpio.output(self._pinOut, self._initialState)


        Thread.__init__(self, *args, **kwargs)

        self._readInterval = readInterval

        self._run = True

        self._waitTime = waitTime

        self._logger = logging.getLogger(self._label)
        self._logger.setLevel(logging.DEBUG)
                
        self._logger.info(self._label + ' started')


    @property
    def state(self):
        return self._state


    @state.setter
    def state(self, value):
        self._state = value


    @property
    def pinIn(self):
        return self._pinIn


    @property
    def pinOut(self):
        return self._pinOut


    @property
    def initialState(self):
        return self._initialState


    def set(self):
        self._gpio.output(self._pinOut, self._state)


    @property
    def label(self):
        return self._label


    @property
    def gpio(self):
        return self._gpio


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


    def distance(self):
        self._gpio.output(self._pinOut, LOW)
        time.sleep(self._readInterval)
        self._gpio.output(self._pinOut, HIGH)
        time.sleep(self._readInterval*7.5)
        self._gpio.output(self._pinOut, LOW)

        t3 = time.time()
        while not self._gpio.input(self._pinIn):
            t4 = time.time()
            if (t4 - t3) > 0.03:
                return -1

        t1 = time.time()
        while self._gpio.input(self._pinIn):
            t5 = time.time()
            if (t5 - t1) > 0.03:
                return -1

        t2 = time.time()
        time.sleep(self._readInterval*500)

        time.sleep(self._readInterval*500)
        return ((t2 - t1) * 340 / 2) * 100


