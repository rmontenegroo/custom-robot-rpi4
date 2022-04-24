import time
import logging

from threading import Thread

from robot.component import OnOffComponent

logging.basicConfig(format='%(asctime)s %(levelname)s (%(process)d) %(filename)s %(funcName)s %(message)s')

OFF = 1
ON = 0
WAITTIME = 0.05


class Buzzer(OnOffComponent, Thread):
    
    """
        Buzzer component
    """
    
    def __init__(self, label, gpio, pin, initialState=None, waitTime = WAITTIME, *args, **kwargs):
        
        OnOffComponent.__init__(self, label, gpio, pin, ON, OFF, initialState)
        
        Thread.__init__(self, *args, **kwargs)

        self._beeps = 0

        self._run = True

        self._state = OFF

        self._waitTime = waitTime
        self._initialWaitTime = waitTime
        
        self._logger = logging.getLogger(self._label)
        self._logger.setLevel(logging.DEBUG)
                
        self._logger.info(self._label + ' started')
    
                    
    def beep(self, beeps=1, waitTime=0.25):
        self._logger.info(self._label)

        if self._beeps == 0:
            self._beeps = 2*beeps

        if waitTime:
            self._waitTime = waitTime
            
        
    def stop(self):
        self._logger.info(self._label)
        self._run = False


    def set(self):
        if self._beeps == 0:
            self._waitTime = self._initialWaitTime

        elif self._beeps > 0:
            self._state = ON if self._beeps % 2 == 0 else OFF
            self._beeps -= 1
        
        self._gpio.write(self._pin, self._state)


    def off(self):
        self._beeps = 0
        self._waitTime = self._initialWaitTime
        self._state = OFF

    
    def run(self):
        self._logger.info(self._label)
                
        try:
            
            while self._run or self._beeps > 0:
                                        
                self.set()
                            
                time.sleep(self._waitTime)
                
        except Exception as e :
            self._logger.info(self._label + ' exception')
            raise e
            
        finally:
            self._logger.info(self._label + ' finally')
            self.off()
            self.set()  


