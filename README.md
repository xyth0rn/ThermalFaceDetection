# ThermalFaceDetection

## [1] MLX90640 setup

### [1-1] install Jetson.GPIO
https://github.com/NVIDIA/jetson-gpio
```
$ sudo pip3 install Jetson.GPIO
$ sudo apt-get install -y libi2c-dev i2c-tools
```
use this command to check I2C bus device
```
$ sudo i2cdetect -y -r 1
```
result:
```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- 33 -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
```

### [1-2] install adafruit library
```
$ sudo apt-get install -y python-smbus
$ sudo pip3 install adafruit-blinka
$ sudo pip3 install adafruit-circuitpython-mlx90640
```

### [1-3] MLX90640 & jetson nano connect

the connections between Jetson Nano & MLX90640

![alt text](https://github.com/NicoIsAwesome/ThermalFaceDetection/blob/main/nano_mlx.png)

circuit recommended by Melexis

![alt text](https://github.com/NicoIsAwesome/ThermalFaceDetection/blob/main/mlx90640_cir.png)

Jeson Nano GPIO map

![alt text](https://github.com/NicoIsAwesome/ThermalFaceDetection/blob/main/Jetson_Nano_GPIO.png)

### [1-4] optional: use EasyEDA & CNC to create a simple circuit board
Schematics
![alt text](https://github.com/NicoIsAwesome/ThermalFaceDetection/blob/main/mlx90640_sch.png)

Layout
![alt text](https://github.com/NicoIsAwesome/ThermalFaceDetection/blob/main/mlx90640_lay.png)

CNC
![alt text](https://github.com/NicoIsAwesome/ThermalFaceDetection/blob/main/pcb_1.jpeg)
![alt text](https://github.com/NicoIsAwesome/ThermalFaceDetection/blob/main/pcb_2.jpeg)
![alt text](https://github.com/NicoIsAwesome/ThermalFaceDetection/blob/main/pcb_3.jpeg)

### [1-5] the assembly of MLX90640 FLIR, camera and Jeson Nano
![alt text](https://github.com/NicoIsAwesome/ThermalFaceDetection/blob/main/pcb_4.jpeg)
![alt text](https://github.com/NicoIsAwesome/ThermalFaceDetection/blob/main/pcb_5.jpeg)

There are 2 versions of MLX90640. FOV 55 & FOV 110.  I use FOV 110
Need to choose a camera with FOV 110.

## [2] Python Programs (Python3 only)

### [2-1] 1_mlx90640.py

![alt text]()

### [2-2] 2_cam_overlay_mlx.py
If the FOV of your camera is not perfect match with the FOV of MLX90640, you can use this program to check the difference of FOV. 
![alt text]()

### [2-3] 3_thermalFaceDetection_1.py
the simplest version, use jetson.inference & facenet face detection.
the resulotion of jetson.utils.videoSource("csi://0") is 16:9 (PS: 4:3 resolution is too high)
the resulotion of MLX90640 is 4:3
.....
![alt text]()

### [2-4] 4_thermalFaceDetection_2.py
"This model is based on Single-Shot-Multibox detector and uses ResNet-10 Architecture as backbone."
use cv2.dnn.readNetFromCaffe.
![alt text]()

## Youtube link

## Reference
Melexis MLX90640:
https://www.melexis.com/en/product/mlx90640/far-infrared-thermal-sensor-array
https://www.reddit.com/r/JetsonNano/comments/jkrjye/mlx90640_32x24_interpolated_to_640x480_on_the/

Hello AI World: 
https://github.com/dusty-nv/jetson-inference#hello-ai-world

LearnOpenCV: Face Detection – OpenCV, Dlib and Deep Learning ( C++ / Python )
https://learnopencv.com/face-detection-opencv-dlib-and-deep-learning-c-python/
https://www.pyimagesearch.com/2017/10/16/raspberry-pi-deep-learning-object-detection-with-opencv/

pyimagesearch: Face detection with OpenCV and deep learning
https://www.pyimagesearch.com/2018/02/26/face-detection-with-opencv-and-deep-learning/


