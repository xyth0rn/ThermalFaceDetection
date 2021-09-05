# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
from multiprocessing import Process
from multiprocessing import Queue
import numpy as np
import argparse
import imutils
import time
import cv2

import time,board,busio
import adafruit_mlx90640
import datetime as dt

def gstreamer_pipeline(
    #capture_width=3280,
    #capture_height=2464,
    capture_width=1640,
    capture_height=1232,
    display_width=640,
    display_height=480,
    framerate=29.999999,
    flip_method=6,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000) # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ # 16Hz max

mlx_shape = (24,32)
tdata = np.zeros((24*32,))
t_img = (np.reshape(tdata,mlx_shape))
rects = None


def temp2Que(tempQueue):
    while True:
        mlx.getFrame(tdata) # read MLX temperatures into frame var
        t_img = (np.reshape(tdata,mlx_shape)) # reshape to 24x32 print(t_img.shape) => (24, 32)
        tempQueue.put(t_img)

def classify_frame(net, inputQueue, outputQueue):
    # keep looping
    while True:
        # check to see if there is a frame in our input queue
        if not inputQueue.empty():
            # grab the frame from the input queue, resize it, and
            # construct a blob from it
            frame = inputQueue.get()
            frame = imutils.resize(frame, width=640)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rects = net.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=7, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
            outputQueue.put(rects)

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


# initialize multiprocessing
inputQueue = Queue(maxsize=1)
outputQueue = Queue(maxsize=1)
detections = None
tempQueue = Queue(maxsize=1)

print("[INFO] starting face detection process...")
p0 = Process(target=classify_frame, args=(net, inputQueue, outputQueue,))
p0.daemon = True
p0.start()

print("[INFO] starting thermal detection process...")
p1 = Process(target=temp2Que, args=(tempQueue,))
p1.daemon = True
p1.start()

print("[INFO] starting video stream...")
cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
time.sleep(2.0) # allow the camera sensor to warm up for 2 seconds
fps = FPS().start()

# loop over the frames from the video stream
while True:
    ret, frame = cap.read()
    #(fh, fw) = frame.shape[:2]
    if inputQueue.empty(): inputQueue.put(frame)
    if not outputQueue.empty(): rects = outputQueue.get()
    if not tempQueue.empty(): t_img = tempQueue.get()

    if (rects is not None) and (t_img is not None):
        for (x, y, w, h) in rects:
            if (w<40) or (h<40): break
            (y1, y2, x1, x2) = ( int(y/20), int((y+h)/20), int(x/20), int((x+w)/20) )
            tmax = t_img[y1:y2, x1:x2].max()
            text = "Tmax={:.1f} C".format(tmax)
            texty = y - 10 if y - 10 > 10 else y + 10
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, text, (x, texty), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
    
    # show the output frame
    cv2.imshow('Face Temperature', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cap.release()
cv2.destroyAllWindows()


