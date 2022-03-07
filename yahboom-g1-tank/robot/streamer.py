#!/bin/env python3

from flask import Flask, render_template, Response
import cv2
from multiprocessing import Process
import time

import logging

logging.basicConfig(format='%(asctime)s %(levelname)s (%(process)d) %(filename)s %(funcName)s %(message)s')

app = Flask('robot.streamer')

def gen_frames():  

    camera = cv2.VideoCapture('/dev/video0')

    camera.set(cv2.CAP_PROP_FPS, 19)    
    camera.set(cv2.CAP_PROP_BUFFERSIZE, 2)

    while True:

        success, frame = camera.read()

        if not success:
            pass

        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' 
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('index.html')


class Streamer(Process):

    def __init__(self, waitTime=0.0001):
        Process.__init__(self)

        self._label = 'robot.streamer'
        self._logger = logging.getLogger(self._label)
        self._logger.setLevel(logging.DEBUG)

        self._waitTime = waitTime
        self._run = True


    def stop(self):
        self._logger.info(self._label)
        # self._run = False
        # Thread.kill(self)
        Process.kill(self)



    def run(self):
        self._logger.info(self._label)

        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False, threaded=True)

        """
        print('aqui')

        try:

            while self._run:

                time.sleep(self._waitTime)

        except Exception as e :
            self._logger.info(self._label + ' exception')
            raise e

        finally:
            self._logger.info(self._label + ' finally')
        """
