import os
from pathlib import Path
from flask import Flask, render_template, Response
from camera import Camera
from flask import request
import json
IMG_SIZE = (640, 360)

FIFO_PATH_CMD = '/home/pi/fifo_cmd'


app = Flask(__name__)
camera = Camera()


def streaming():
    global camera
    while True:
        frame = camera.get_frame()
        # frame = camera.get_frame_test()
        if len(frame) > 0:

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def send_cmd(cmd):
    with open(FIFO_PATH_CMD, 'w') as fifo:
        for c in cmd:
            fifo.flush()
            fifo.write(c)
            fifo.write('\n')


@app.route('/')
def index():
    send_cmd(['manual', 'stop'])
    return render_template('index.html')


@app.route('/postmethod', methods=['POST'])
def get_post_javascript_data():
    jsdata = request.form['javascript_data']
    print(jsdata)
    coorArray = jsdata.split()
    x1 = int(float(coorArray[0]))
    y1 = int(float(coorArray[1]))
    x2 = int(float(coorArray[2]))
    y2 = int(float(coorArray[3]))

    xx1 = min(x1, x2)
    yy1 = min(y1, y2)
    xx2 = max(x1, x2)
    yy2 = max(y1, y2)
    
    width = xx2 - xx1
    height = yy2 - yy1

    loc = f'{xx1},{yy1},{width},{height}'
    print(f'select target: {loc}')
    
    cmd = ["select target", loc]
    send_cmd(cmd)

    return jsdata


@app.route('/postmethodRes', methods=['POST'])
def get_post_javascript_datares():
    jsdata = request.form['javascript_data']
    print("manual turning: ")
    cmd = ['manual', 'location', 'reset']
    send_cmd(cmd)

    return jsdata


@app.route('/postmethodLeft', methods=['POST'])
def get_post_javascript_datal():
    jsdata = request.form['javascript_data']
    print("manual turning: left")
    cmd = ['manual', 'location', f'{int(IMG_SIZE[0]/4)},{int(IMG_SIZE[1]/2)}']
    send_cmd(cmd)

    return jsdata


@app.route('/postmethodright', methods=['POST'])
def get_post_javascript_datar():
    jsdata = request.form['javascript_data']
    print("manual turning: right")
    cmd = ['manual', 'location', f'{int(IMG_SIZE[0]*3/4)},{int(IMG_SIZE[1]/2)}']
    send_cmd(cmd)

    return jsdata


@app.route('/postmethodup', methods=['POST'])
def get_post_javascript_datau():
    jsdata = request.form['javascript_data']
    print("manual turning: up")
    cmd = ['manual', 'location', f'{int(IMG_SIZE[0]/2)},{int(IMG_SIZE[1]/4)}']
    send_cmd(cmd)

    return jsdata


@app.route('/postmethoddown', methods=['POST'])
def get_post_javascript_datad():
    jsdata = request.form['javascript_data']
    print("manual turning: down")
    cmd = ['manual', 'location', f'{int(IMG_SIZE[0]/2)},{int(IMG_SIZE[1]*3/4)}']
    send_cmd(cmd)

    return jsdata


@app.route('/ManualMode')
def ManualMode():
    # send a signal to motorcontroller/otherthings to alert camera to change mode
    send_cmd(['manual', 'start'])
    return render_template('ManualMode.html')


@app.route('/SelectTarget')
def SelectTarget():
    # send a signal to motorcontroller/otherthings to alert camera to change mode
    return render_template('SelectTarget.html')


@app.route('/video_feed')
def video_feed():
    return Response(streaming(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
