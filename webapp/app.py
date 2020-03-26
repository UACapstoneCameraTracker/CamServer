from flask import Flask, render_template, Response
from camera import Camera
from flask import request
import json
from motor_control import gimbal
IMG_SIZE = (640, 360)
FIFO_PATH_CMD = '/home/pi/fifo_cmd'



app = Flask(__name__)
gimbal.init_gimbal(IMG_SIZE)
camera = Camera()


def streaming():
    global camera
    while True:
        frame = camera.get_frame()
        # frame = camera.get_frame_test()
        if len(frame) > 0:

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')




@app.route('/postmethod', methods=['POST'])
def get_post_javascript_data():
    jsdata = request.form['javascript_data']
    print(jsdata)
    coorArray = jsdata.split()
    x1 = coorArray[0]
    y1 = coorArray[1]
    x2 = coorArray[2]
    y2 = coorArray[3]
    width = str(float(x2) -float(x1))
    height = str(float(y2)- float(y1))

    print("x1: " + x1 + " y1: " + y1 + " x2: " + x2 + " y2:" + y2)
    print("x1: " + x1 + " y1: " + y1 + " width: " + width + " height: " + height)

    cmd = "select target"
    bbox = x1+","+y2+","+height+","+width

    with open(FIFO_PATH_CMD, 'w') as fifo:
        fifo.flush()
        fifo.write(cmd)
        fifo.write('\n')
        fifo.write(bbox)

    fifo.close()


    return jsdata

@app.route('/postmethodRes', methods=['POST'])
def get_post_javascript_datares():
    jsdata = request.form['javascript_data']
    print("manual turning: ")
    print(jsdata)

    print("call gimbal ini to reset ")
    gimbal.init_gimbal(IMG_SIZE)

    return jsdata

@app.route('/postmethodLeft', methods=['POST'])
def get_post_javascript_datal():
    jsdata = request.form['javascript_data']
    print("manual turning: left")
    print(jsdata)

    print("call gimbal.move_to((....)) or switch to pipe later ")
    gimbal.move_to((-IMG_SIZE[0]/4, IMG_SIZE[1]/2))

    return jsdata

@app.route('/postmethodright', methods=['POST'])
def get_post_javascript_datar():
    jsdata = request.form['javascript_data']
    print("manual turning: right")
    print(jsdata)
    print("call gimbal.move_to( .... ) or switch to pipe later ")
    gimbal.move_to((IMG_SIZE[0]*3/4, IMG_SIZE[1]/2))

    return jsdata


@app.route('/postmethodup', methods=['POST'])
def get_post_javascript_datau():
    jsdata = request.form['javascript_data']
    print("manual turning: up")
    print(jsdata)
    print("call gimbal.move_to(.... ) or switch to pipe later ")
    gimbal.move_to((IMG_SIZE[0]/2, IMG_SIZE[1]/4))

    return jsdata


@app.route('/postmethoddown', methods=['POST'])
def get_post_javascript_datad():
    jsdata = request.form['javascript_data']
    print("manual turning: down")
    print(jsdata)
    print("call gimbal.move_to(.... ) or switch to pipe later ")
    gimbal.move_to((IMG_SIZE[0]/2, IMG_SIZE[1]*3/4))

    return jsdata




@app.route('/ManualMode')
def ManualMode():
    # send a signal to motorcontroller/otherthings to alert camera to change mode
    return render_template('ManualMode.html')







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


def send_moving_cmd(moving_cmd):
    cmd = "manual"
    with open(FIFO_PATH_CMD, 'w') as fifo:
        fifo.flush()
        fifo.write(cmd)
        fifo.write('\n')
        fifo.write(moving_cmd)

    fifo.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
