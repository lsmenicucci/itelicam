from . import yolo
from threading import Thread
import cv2

DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 360

class WebcamVideoStream:
    def __init__(self, src=0):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        self.stream.set(3, DEFAULT_WIDTH)
        self.stream.set(4, DEFAULT_HEIGHT)
        (self.grabbed, self.frame) = self.stream.read()

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self
    
    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
			# if the thread indicator variable is set, stop the thread
            if self.stopped:
                return
            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()
	
    def read(self):
        # return the frame most recently read
        return self.frame
 
    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

class DetectionVideoStream(WebcamVideoStream):
    def __init__(self):
        super().__init__()
        self.yolo_nn = yolo.YOLO_NN('vprocess/yolov3')
    
    def update(self):
        global N_PERSONS,QUEUE
         # keep looping infinitely until the thread is stopped
        while True:
			# if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()
            status, states, draw_frame = self.yolo_nn.detect(self.frame)

            QUEUE.put(self.frame)
