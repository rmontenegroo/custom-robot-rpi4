import time
import logging

from threading import Thread

from robot.component import OnOffComponent


logging.basicConfig(format='%(asctime)s %(levelname)s (%(process)d) %(filename)s %(funcName)s %(message)s')

ON = 1
OFF = 0


class Led(OnOffComponent, Thread):
    
    """
        Led component
    """
    
    def __init__(self, label, gpio, pin, initialState=None, waitTime = 0.05, *args, **kwargs):
        
        OnOffComponent.__init__(self, label, gpio, pin, ON, OFF, initialState)
        
        Thread.__init__(self, *args, **kwargs)

        self._blinks = 0

        self._run = True

        self._waitTime = waitTime
        self._initialWaitTime = waitTime
        
        self._logger = logging.getLogger(self._label)
        self._logger.setLevel(logging.DEBUG)
                
        self._logger.info(self._label + ' started')


    def blink(self, blinks=1, waitTime=0.25):
        self._logger.info(self._label)

        if self._blinks == 0:
            self._blinks = 2*blinks

        if waitTime:
            self._waitTime = waitTime

        
    def stop(self):
        self._logger.info(self._label)
        self._run = False


    def set(self):
        if self._blinks == 0:
            self._waitTime = self._initialWaitTime

        elif self._blinks > 0:
            self._state = ON if self._blinks % 2 == 0 else OFF
            self._blinks -= 1
        
        self._gpio.write(self._pin, self._state)


    def off(self):
        self._blinks = 0
        self._waitTime = self._initialWaitTime
        self._state = OFF
    

    def run(self):
        self._logger.info(self._label)
                
        try:
            
            while self._run or self._blinks > 0:
                                        
                self.set()
                            
                time.sleep(self._waitTime)
                
        except Exception as e :
            self._logger.info(self._label + ' exception')
            raise e
            
        finally:
            self._logger.info(self._label + ' finally')
            self.off()
            self.set()  
    
