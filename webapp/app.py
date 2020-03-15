from flask import Flask,render_template,Response
from cam_base import Base_Camera
# from motor_control import gimbal

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        # frame = camera.get_frame_test()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n')

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
    return Response(gen(Base_Camera()),
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
