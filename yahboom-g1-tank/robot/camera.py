import cv2
import time
import logging
import os
import random
import string

from threading import Thread, Lock

logging.basicConfig(format='%(asctime)s %(levelname)s (%(process)d) %(filename)s %(funcName)s %(message)s')


class Camera(Thread):
    

    def __init__(self, label, deviceName = '/dev/video0', waitTime = 0.01):

        Thread.__init__(self)

        self._captureDevice = cv2.VideoCapture(deviceName)
        self._deviceName = deviceName
        self._snapshotLock = Lock()
        self._snapCountLock = Lock()
        self._label = label
        self._lastSnapshot = None

        self.__snapCount = 0
        self.__rndPrefix = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))

        self._waitTime = waitTime

        self._run = True

        self._logger = logging.getLogger(self._label)
        self._logger.setLevel(logging.DEBUG)

        self._logger.info(self._label + ' started')


    def clear(self):
        self._logger.info(self._label)
        self._captureDevice.release()
        self._logger.info('camera released')


    @property
    def deviceName(self):
        return self._deviceName


    @property
    def label(self):
        return self._label


    def stop(self):
        self._logger.info(self._label)
        self._run = False


    def set(self):
       pass 


    def run(self):
        try:

            while self._run:

                self._snapshotLock.acquire()
                ret, frame = self._captureDevice.read()
                self._snapshotLock.release()
                self._lastSnapshot = frame

                self.set()

                # time.sleep(self._waitTime)

        except Exception as e :
            self._logger.info(self._label + ' exception')
            raise e

        finally:
            self._logger.info(self._label + ' finally')
            self.clear()


    def lastFrame(self):
        self._logger.info(self._label)
        frame = None
        print('xxxxxxxxxxxxxxxx iuiuaiuia')
        # if self._snapshotLock.acquire(blocking=False):
        print('uiuiuaiuia')
        frame = self._lastSnapshot
        #    self._snapshotLock.release()
        print('LastFrame', frame)
        return frame

    def snapshot(self, dirname='/tmp', filename='snapshot.jpg', overwrite=True):
        self._logger.info(self._label)

        frame = self.lastFrame()

        if frame is not None:

            filepath = os.path.join(dirname, f'{filename}')

            if not overwrite:

                self._snapCountLock.acquire()
                filepath = os.path.join(dirname, f'{self.__rndPrefix}_{self.__snapCount}_{filename}')
                self._snapCountLock.release()

            cv2.imwrite(filepath, frame)

            self._snapCountLock.acquire()
            self.__snapCount += 1
            self._snapCountLock.release()

            self._logger.info(f'Snapshot captured to {filepath}.')

        else:
            self._logger.error(f'It was not possible to capture image from camera {self._deviceName}.')
        

