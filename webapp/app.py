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
    width = int(x2)-int(x1)
    height = int(y2)-int(y1)

    print("x1: " + x1 + " y1: " + y1 + " x2: " + x2 + " y2:" + y2)
    print("x1: " + x1 + " y1: " + y1 + " width: " + width + " height: " + height)

    cmd = "select target"
    bbox = cod1+","+cod2+","+lenth+","+width

    with open(FIFO_PATH_CMD, 'w') as fifo:
        fifo.flush()
        fifo.write(cmd)
        fifo.write('\n')
        fifo.write(bbox)

    fifo.close()


    return jsdata


@app.route('/postmethodLeft', methods=['POST'])
def get_post_javascript_datal():
    jsdata = request.form['javascript_data']
    print("manual turning: ")
    print(jsdata)
    
    print("call gimbal.move_to((-100,0)) or switch to pipe later ")
    gimbal.move_to((IMG_SIZE[0]/4, IMG_SIZE[1]/2))
    
    return jsdata

@app.route('/postmethodright', methods=['POST'])
def get_post_javascript_datar():
    jsdata = request.form['javascript_data']
    print("manual turning: ")
    print(jsdata)
    print("call gimbal.move_to( .... ) or switch to pipe later ")
    gimbal.move_to((IMG_SIZE[0]/4, IMG_SIZE[1]/2))
    
    return jsdata


@app.route('/postmethodup', methods=['POST'])
def get_post_javascript_datau():
    jsdata = request.form['javascript_data']
    print("manual turning: ")
    print(jsdata)
    print("call gimbal.move_to(.... ) or switch to pipe later ")
    gimbal.move_to((IMG_SIZE[0]/4, IMG_SIZE[1]/2))
    
    return jsdata


@app.route('/postmethoddown', methods=['POST'])
def get_post_javascript_datad():
    jsdata = request.form['javascript_data']
    print("manual turning: ")
    print(jsdata)
    print("call gimbal.move_to(.... ) or switch to pipe later ")
    gimbal.move_to((IMG_SIZE[0]/4, IMG_SIZE[1]/2))
    
    return jsdata



# @app.route('/CruisingMode')
# def CruisingMode():
#     # send a signal to motorcontroller/otherthings to alert camera to change mode
#     return render_template('CruisingMode.html')


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



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    












# from flask import Flask, render_template, Response
# from camera import Camera
# from flask import request
# import json
# # from motor_control import gimbal

# from motor_control import gimbal



# app = Flask(__name__)
# gimbal.init_gimbal((360,640))
# camera = Camera()

# FIFO_PATH_CMD = '/home/pi/fifo_cmd'


# def streaming():
#     global camera
#     while True:
#         frame = camera.get_frame()
#         # frame = camera.get_frame_test()
#         if len(frame) > 0:
            
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# @app.route('/')
# def index():
#     return render_template('index.html')


# # @app.route('/getmethod/<jsdata>')
# # def get_javascript_data(jsdata):
# #     return 12345
# #     # return json.loads(jsdata)
# #     # return jsdata


# @app.route('/postmethod', methods=['POST'])
# def get_post_javascript_data():
#     jsdata = request.form['javascript_data']
#     print(jsdata)
#     coorArray = jsdata.split()
#     x1 = coorArray[0]
#     y1 = coorArray[1]
#     x2 = coorArray[2]
#     y2 = coorArray[3]
#     print("x1: " + x1 + " y1: " + y1 + " x2: " + x2 + " y2:" + y2)
#     return jsdata


# @app.route('/SendPost', methods=['POST'])
# def Send_post():
#     jsdata = request.form['javascript_data']
#     # print(jsdata)
#     coorArray = jsdata.split()
#     x1 = coorArray[0]
#     y1 = coorArray[1]
#     x2 = coorArray[2]
#     y2 = coorArray[3]
#     # print("x1: " + x1 + " y1: " + y1 + " x2: " + x2 + " y2:" + y2)
    
#     cod1 = string(int(float(x1)))
#     cod2 = string(int(float(y1)))
#     width = string(int(float(x2)-float(x1)))
#     height = string(int(float(y2)-float(y1)))

#     cmd = "select target"
#     bbox = cod1+","+cod2+","+lenth+","+width
#     with open(FIFO_PATH_CMD, 'w') as fifo:
#         fifo.flush()
#         fifo.write(cmd)
#         fifo.write('\n')
#         fifo.write(bbox)

#     fifo.close()

#     return None


# @app.route('/CruisingMode')
# def CruisingMode():
#     # send a signal to motorcontroller/otherthings to alert camera to change mode
#     return render_template('CruisingMode.html')


# @app.route('/ManualMode')
# def ManualMode():
#     # send a signal to motorcontroller/otherthings to alert camera to change mode
#     return render_template('ManualMode.html')

# def send_moving_cmd(moving_cmd):
#     cmd = "manual"
#     with open(FIFO_PATH_CMD, 'w') as fifo:
#         fifo.flush()
#         fifo.write(cmd)
#         fifo.write('\n')
#         fifo.write(moving_cmd)

#     fifo.close()


# @app.route('/turnleft')
# def turnleft():
#     # send a signal to motorcontroller/otherthings to alert camera to change mode
    
#     print("call motor to turn left ")

#     send_moving_cmd("start")

#     gimbal.move_to((-100,0))
#     return render_template('ManualMode.html')
#     # return "nothing"


# @app.route('/turnright')
# def turnright():
#     # send a signal to motorcontroller/otherthings to alert camera to change mode
#     send_moving_cmd("start")
#     gimbal.move_to((100,0))
#     print("call motor to turn right ")
#     return render_template('ManualMode.html')


# @app.route('/turnup')
# def turnup():
#     # send a signal to motorcontroller/otherthings to alert camera to change mode
#     send_moving_cmd("start")
#     gimbal.move_to((0,100))
#     print("call motor to turn up ")
#     return render_template('ManualMode.html')


# @app.route('/turndown')
# def turndown():
#     # send a signal to motorcontroller/otherthings to alert camera to change mode
#     send_moving_cmd("start")
#     print("call motor to turn down ")
#     gimbal.move_to((0,-100))
#     return render_template('ManualMode.html')
#     # return "nothing"


# @app.route('/stopturning')
# def stopturning():
#     # send a signal to motorcontroller/otherthings to alert camera to change mode
#     print("call motor to stop turning ")
#     send_moving_cmd("stop")
#     gimbal.init_gimbal((360,640))
#     return render_template('ManualMode.html')
#     # return "nothing"


# @app.route('/SelectTarget')
# def SelectTarget():
#     # send a signal to motorcontroller/otherthings to alert camera to change mode
#     return render_template('SelectTarget.html')


# @app.route('/video_feed')
# def video_feed():
#     return Response(streaming(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')
# # The secret to implement in-place updates is to use a multipart response.
# # Multipart responses consist of a header that includes one of the multipart content types,
# # followed by the parts,
# # separated by a boundary marker and each having its own part specific content type.
# # There are several multipart content types for different needs.
# # For the purpose of having a stream where each part replaces the previous part the
# # multipart/x-mixed-replace content type must be used.


# # need to manually change the host ip address to pi's local ip address
# # so under the same wifi, ie, http://192.168.1.64:5000 to connect
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')
    