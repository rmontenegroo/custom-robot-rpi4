import cv2
import time
import os
import random
import logging
import string
import queue

from flask import Flask, render_template, Response
from threading import Thread


logging.basicConfig(format='%(asctime)s %(levelname)s (%(process)d) %(filename)s %(funcName)s %(message)s')


class Streamer(Thread):


    def __init__(self, deviceName='/dev/video0', fps=19, webServerPort=5000, flipH=True, flipV=True, waitTime=0.01):
        Thread.__init__(self)

        self._label = 'robot.streamer'

        self._deviceName = deviceName
        self._fps = fps

        self._flipV = True
        self._flipH = True

        self._webServer = None
        self._webServerPort = webServerPort

        self._camera = cv2.VideoCapture(deviceName)
        self._camera.set(cv2.CAP_PROP_FPS, fps)

        self._takeSnapshot = False

        self._frame_queue = queue.Queue(fps+1)

        self._frame_reader_thread = Thread(target=self._frame_reader, daemon=True)
        self._frame_reader_thread.start()

        self._flask = Flask(self._label)
        self._flask.add_url_rule('/', 'index', view_func=self.index)
        self._flask.add_url_rule('/video_feed', 'video_feed', view_func=self.video_feed)

        self._snapCount = 0
        self._rndPrefix = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))

        self._logger = logging.getLogger(self._label)
        self._logger.setLevel(logging.DEBUG)

        self._waitTime = waitTime
        self._run = True


    def stop(self):
        self._logger.info(self._label)
        self._run = False
        self._camera.release()


    def _frame_reader(self):

        while True:

            ret, frame = self._camera.read()

            if frame is not None:

                if self._frame_queue.full():
                    while not self._frame_queue.empty(): self._frame_queue.get()

                if self._flipV:
                    frame = cv2.flip(frame, 0)

                if self._flipH:
                    frame = cv2.flip(frame, 1)

                if self._takeSnapshot:
                    self._save_snapshot(frame, self._snapshotDirname, self._snapshotFilename, self._snapshotOverwrite)
                    self._takeSnapshot = False

                self._frame_queue.put_nowait(frame)


    @property
    def flask(self):
        return self._flask


    def _gen_frame(self):

        while True:
            if not self._frame_queue.empty():
                frame = self._frame_queue.get_nowait()

                ret, frame = cv2.imencode('.jpg', frame)
                frame = frame.tobytes()
                yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


    def video_feed(self):
        return Response(self._gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


    def index(self):
        return render_template('index.html')


    def run(self):
        self._logger.info(self._label)

        self._webServer = Thread(daemon=True, target=self._flask.run, kwargs={'host':'0.0.0.0', 'port': self._webServerPort, 'debug': False, 'use_reloader': False, 'threaded': True})
        self._webServer.start()

        while self._run:

            time.sleep(self._waitTime)


    def snapshot(self, dirname='/tmp', filename='snapshot.jpg', overwrite=True):
        self._snapshotDirname = dirname
        self._snapshotFilename = filename
        self._snapshotOverwrite = overwrite
        self._takeSnapshot = True


    def _save_snapshot(self, frame, dirname, filename, overwrite):
        self._logger.info(self._label)

        if frame is not None:

            filepath = os.path.join(dirname, f'{filename}')

            if not overwrite:
                filepath = os.path.join(dirname, f'{self._rndPrefix}_{self._snapCount}_{filename}')

            cv2.imwrite(filepath, frame)

            self._snapCount += 1

            self._logger.info(f'Snapshot captured to {filepath}.')

        else:
            self._logger.error(f'It was not possible to capture image from camera {self._deviceName}.')





