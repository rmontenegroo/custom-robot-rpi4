import cv2
import time
import copy
import os
import random
import logging
import string
import hashlib

from flask import Flask, render_template, Response
from multiprocessing import Process
from threading import Thread, Lock

logging.basicConfig(format='%(asctime)s %(levelname)s (%(process)d) %(filename)s %(funcName)s %(message)s')


class Streamer(Thread):


    def __init__(self, deviceName='/dev/video0', waitTime=0.01):
        Thread.__init__(self)

        self._label = 'robot.streamer'

        self._webServer = None

        self._camera = cv2.VideoCapture(deviceName)
        self._camera.set(cv2.CAP_PROP_FPS, 19)

        while not self._camera.isOpened(): time.sleep(0.1)

        self._lastFrame = self._camera.read()[1]
        self._frameLock = Lock()

        self._flask = Flask('robot.streamer')
        self._flask.add_url_rule('/', 'index', view_func=self.index)
        self._flask.add_url_rule('/video_feed', 'video_feed', view_func=self.video_feed)

        self.__snapCount = 0
        self.__rndPrefix = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))

        self._logger = logging.getLogger(self._label)
        self._logger.setLevel(logging.DEBUG)

        self._waitTime = waitTime
        self._run = True


    def stop(self):
        self._logger.info(self._label)

        self._run = False

        if self._webServer is not None:
            self._webServer.kill()

        self._camera.release()


    @property
    def lastFrame(self):
        # self._logger.info(self._label)
        self._frameLock.acquire()
        frame = copy.copy(self._lastFrame)
        self._frameLock.release()
        return frame


    @lastFrame.setter
    def lastFrame(self, value):
        # self._logger.info(self._label)
        self._frameLock.acquire()
        self._lastFrame = value
        self._frameLock.release()


    def __generate_frame(self):

        while True:

            ret, frame = self._camera.read()

            if frame is not None:

                self.lastFrame = frame

                m = hashlib.sha256()
                m.update(frame)
                print('###', m.hexdigest())

                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


    @property
    def flask(self):
        return self._flask


    def video_feed(self):
        return Response(self.__generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


    def index(self):
        return render_template('index.html')


    def run(self):
        self._logger.info(self._label)

        self._webServer = Process(daemon=True, target=self._flask.run, kwargs={'host':'0.0.0.0', 'port': 5000, 'debug': False, 'use_reloader': False, 'threaded': True})
        self._webServer.start()

        while self._run:

            time.sleep(self._waitTime)


    def snapshot(self, dirname='/tmp', filename='snapshot.jpg', overwrite=True):
        self._logger.info(self._label)

        frame = self.lastFrame

        if frame is not None:

            print('#'*100)

            filepath = os.path.join(dirname, f'{filename}')

            if not overwrite:
                filepath = os.path.join(dirname, f'{self.__rndPrefix}_{self.__snapCount}_{filename}')

            cv2.imwrite(filepath, frame)

            self.__snapCount += 1

            self._logger.info(f'Snapshot captured to {filepath}.')

        else:
            self._logger.error(f'It was not possible to capture image from camera {self._deviceName}.')





