import time

class Base_Camera(object):
    
    # def __init__(self):
    #     # emulate camera
    #     # later change it to read frames from other thread/file/...
    #     # fpath = "../../"
    #     # self.frames = [open(f + '.jpg', 'rb').read() for f in ['1', '2', '3']]
    #     self.frames = [open('/home/pi/Desktop/img.png').read()]
        
    def get_frame(self):
        # int time() returns 1582079059 
        # return self.frames[int(time.time()) % 3]
        frames = open('/home/pi/fifo_img.jpg','rb').read()
        return frames

    # this is the server testing function. 
    # send three sample image through the server instead of the real camera feed
    def get_frame_test(self):
        frames = [open(f + '.jpg', 'rb').read() for f in ['1', '2', '3']]
        # frames = open('1.jpg','rb').read()
        return frames[int(time.time()) % 3]
