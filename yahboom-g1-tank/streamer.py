#!/bin/env python3

from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

def gen_frames():  # generate frame by frame from camera

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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

