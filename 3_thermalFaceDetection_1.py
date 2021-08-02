import jetson.inference
import jetson.utils

import numpy as np
import time,board,busio
import adafruit_mlx90640
import datetime as dt

from multiprocessing import Process
from multiprocessing import Queue

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000) # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_8_HZ # 16Hz max
tdata = np.zeros((24*32,))

def temp2Que(tempQueue):
    while True:
        mlx.getFrame(tdata) # read MLX temperatures into frame var
        t_img = (np.reshape(tdata[96:672],(18,32))) # reshape to 18x32, print(t_img.shape) => (18, 32)
        tempQueue.put(t_img)

tempQueue = Queue(maxsize=1)
p1 = Process(target=temp2Que, args=(tempQueue,))
p1.daemon = True
p1.start()

net = jetson.inference.detectNet("facenet", threshold=0.3)
camera = jetson.utils.videoSource("csi://0", argv=["--input-flip=vertical"])
display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file
font = jetson.utils.cudaFont()

time.sleep(2.0) # allow the camera sensor to warm up for 2 seconds

while display.IsStreaming():
    img = camera.Capture()
    detections = net.Detect(img, overlay="box")
    if not tempQueue.empty(): t_img = tempQueue.get()
    if (detections is not None) and (t_img is not None):
        for detection in detections:
            box = np.array([int(detection.Left), int(detection.Top), int(detection.Right), int(detection.Bottom)])/40
            (startX, startY, endX, endY) = box.astype("int")
            if startX>0 : startX -= 1
            if startY>0 : startY -= 1          
            if endX <32 : endX += 1
            if endY <18 : endY += 1
            tmax = t_img[startY:endY, startX:endX].max()
            text = "Tmax={:.1f} C".format(tmax)
            font.OverlayText(img, img.width, img.height, text, int(detection.Left), int(detection.Top), font.White, font.Gray40)
    display.Render(img)
    display.SetStatus("Face Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))


