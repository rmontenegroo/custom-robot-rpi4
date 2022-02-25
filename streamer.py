#!/bin/env python3

from flask import Flask, render_template, Response
import cv2
import time

time.sleep(5)

app = Flask(__name__)

def gen_frames():  # generate frame by frame from camera

    camera = cv2.VideoCapture('/dev/video0')

    while True:

        success, frame = camera.read()  # read the camera frame

        if not success:
            pass

        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' 
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

        # time.sleep(0.01)


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=7172, threaded=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
    # camera.release()

