from flask import Flask, render_template, Response
from camera import Camera
from flask import request
import json
# from motor_control import gimbal

app = Flask(__name__)


def streaming():
    camera = Camera()
    while True:
        frame = camera.get_frame()
        if len(frame) > 0:
            # frame = camera.get_frame_test()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/getmethod/<jsdata>')
# def get_javascript_data(jsdata):
#     return 12345
#     # return json.loads(jsdata)
#     # return jsdata


@app.route('/postmethod', methods=['POST'])
def get_post_javascript_data():
    jsdata = request.form['javascript_data']
    print(jsdata)
    coorArray = jsdata.split()
    x1 = coorArray[0]
    y1 = coorArray[1]
    x2 = coorArray[2]
    y2 = coorArray[3]

    print("x1: " + x1 + " y1: " + y1 + " x2: " + x2 + " y2:" + y2)
    return jsdata


@app.route('/CruisingMode')
def CruisingMode():
    # send a signal to motorcontroller/otherthings to alert camera to change mode
    return render_template('CruisingMode.html')


@app.route('/ManualMode')
def ManualMode():
    # send a signal to motorcontroller/otherthings to alert camera to change mode
    return render_template('ManualMode.html')


@app.route('/turnleft')
def turnleft():
    # send a signal to motorcontroller/otherthings to alert camera to change mode
    print("call motor to turn left ")
    return render_template('ManualMode.html')
    # return "nothing"


@app.route('/turnright')
def turnright():
    # send a signal to motorcontroller/otherthings to alert camera to change mode
    print("call motor to turn right ")
    return render_template('ManualMode.html')


@app.route('/turnup')
def turnup():
    # send a signal to motorcontroller/otherthings to alert camera to change mode
    print("call motor to turn up ")
    return render_template('ManualMode.html')


@app.route('/turndown')
def turndown():
    # send a signal to motorcontroller/otherthings to alert camera to change mode
    print("call motor to turn down ")
    return render_template('ManualMode.html')
    # return "nothing"


@app.route('/stopturning')
def stopturning():
    # send a signal to motorcontroller/otherthings to alert camera to change mode
    print("call motor to stop turning ")
    return render_template('ManualMode.html')
    # return "nothing"


@app.route('/SelectTarget')
def SelectTarget():
    # send a signal to motorcontroller/otherthings to alert camera to change mode
    return render_template('SelectTarget.html')


@app.route('/video_feed')
def video_feed():
    return Response(streaming(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
# The secret to implement in-place updates is to use a multipart response.
# Multipart responses consist of a header that includes one of the multipart content types,
# followed by the parts,
# separated by a boundary marker and each having its own part specific content type.
# There are several multipart content types for different needs.
# For the purpose of having a stream where each part replaces the previous part the
# multipart/x-mixed-replace content type must be used.


# need to manually change the host ip address to pi's local ip address
# so under the same wifi, ie, http://192.168.1.64:5000 to connect
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
