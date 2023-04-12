from flask import Response
from flask import Flask
from flask import render_template
import random
import time
import cv2

# initialize a flask object
app = Flask(__name__)
# initialize the video stream and allow the camera sensor to start up
camera_0 = cv2.VideoCapture(0)  # have to double-check which camera is which
camera_1 = cv2.VideoCapture(1)
camera_2 = cv2.VideoCapture(2)
time.sleep(2.0)


@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")


def generate(camera):
    # loop over frames from the output stream
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # yield the output frame in the byte format
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   frame + b'\r\n')


@app.route("/camera0")
def camera0():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(camera_0), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/camera1")
def camera1():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(camera_1), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/camera2")
def camera2():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(camera_2), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.get("/telemetry")
def telemetry():
    print(random.random())
    return str(random.random())


# check to see if this is the main thread of execution
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
