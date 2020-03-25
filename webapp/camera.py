import time

FIFO_PATH = '/home/pi/fifo_img.jpg'


class Camera(object):
    # def __init__(self):
        # self.pipe = open(FIFO_PATH, 'rb')

    def get_frame(self):
        self.pipe = open(FIFO_PATH, 'rb')
        # int time() returns 1582079059
        # return self.frames[int(time.time()) % 3]
        frames = self.pipe.read()
        return frames

    # this is the server testing function.
    # send three sample image through the server instead of the real camera feed
    def get_frame_test(self):
        frames = [open('test/' + f + '.jpg', 'rb').read() for f in ['1', '2', '3']]
        # frames = open('1.jpg','rb').read()
        return frames[int(time.time()) % 3]
