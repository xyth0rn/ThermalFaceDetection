# Thermal-Face Detection
The pandemic has been going on for a while, stores and schools are required to keep track of the people's body temperature to perform preliminary filtration of those who may be in abnormal health conditions. There are some models of automatic thermal scanners on the market with the lowest price starting from 1500 USD. Because of the unaffordable price, the majority of schools and stores still rely on employees checking on people's body temperature one by one. This had me thinking about making a low-cost thermal-face detection device so that schools and local businesses can afford to make one.

The following are photos taken from stores in my city. The two stores in the photos are one of the very few places in my city where machines are used to automatically check people's body temperature. It is worth noting that both machines **CANNOT** perform facial detection. The machines either pinpoint the highest temperature detected, or require the users to position at a specific area in front of the camera.

The machine at the front door of a supermarket.
![alt text](https://github.com/xyth0rn/ThermalFaceDetection/blob/main/photos/market.jpg)
  
The machine at the front door of a shopping mall.
![alt text](https://github.com/xyth0rn/ThermalFaceDetection/blob/main/photos/6plus_plaza.jpg)
  
Close-up view of the actual machine in the previous photo. The result of the machine is transferred to the monitor via cable.
![alt text](https://github.com/xyth0rn/ThermalFaceDetection/blob/main/photos/thermal_machine.jpg)

In this project, I used a MLX90640 Far Infrared Thermal Sensor Array (110° FOV, 32x24 RES) and a 110° FOV camera compatible with the Nvidia Jetson Nano to build a thermal-face detection device. The total cost of the build is around 200 USD.

## [1] MLX90640 Setup

### [1-1] Install Jetson.GPIO
https://github.com/NVIDIA/jetson-gpio
```
$ sudo pip3 install Jetson.GPIO
$ sudo apt-get install -y libi2c-dev i2c-tools
```
Set I2C bus freqeuncy to 400Khz (Must be executed after each reboot) 
```
sudo chmod 666 /sys/bus/i2c/devices/i2c-1/bus_clk_rate
echo 400000 > /sys/bus/i2c/devices/i2c-1/bus_clk_rate
```
You can use the following command to check the I2C bus device.
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

### [1-2] Install Adafruit Library
```
$ sudo apt-get install -y python-smbus
$ sudo pip3 install adafruit-blinka
$ sudo pip3 install adafruit-circuitpython-mlx90640
```

### [1-3] Connections between MLX90640 and the Jetson Nano

Pin connections between the Jetson Nano and MLX90640  
![alt text](https://github.com/xyth0rn/ThermalFaceDetection/blob/main/photos/nano_mlx.png)
  
Circuit recommended by Melexis  
![alt text](https://github.com/xyth0rn/ThermalFaceDetection/blob/main/photos/mlx90640_cir.png)
  
Jeson Nano GPIO map  
![alt text](https://github.com/xyth0rn/ThermalFaceDetection/blob/main/photos/Jetson_Nano_GPIO.png)

### [1-4] Use EasyEDA & CNC to Create a Simple Circuit Board (optional)
I designed the schematics with EasyEDA, then used a simple CNC to make the circuit board.
This step is optional and can be replaced by using breadboard or strip board if CNC is not available.

Schematics  
![alt text](https://github.com/xyth0rn/ThermalFaceDetection/blob/main/photos/mlx90640_sch.png)

Layout  
![alt text](https://github.com/xyth0rn/ThermalFaceDetection/blob/main/photos/mlx90640_lay.png)

CNC  
![alt text](https://github.com/xyth0rn/ThermalFaceDetection/blob/main/photos/pcb_1.jpeg)  
![alt text](https://github.com/xyth0rn/ThermalFaceDetection/blob/main/photos/pcb_2.jpeg)  
![alt text](https://github.com/xyth0rn/ThermalFaceDetection/blob/main/photos/pcb_3.jpeg)  

### [1-5] Assembling MLX90640 FLIR, camera, and the Jetson Nano  
![alt text](https://github.com/xyth0rn/ThermalFaceDetection/blob/main/photos/pcb_4.jpeg)  
![alt text](https://github.com/xyth0rn/ThermalFaceDetection/blob/main/photos/pcb_5.jpeg)

Since I am using a 110° FOV version MLX90640, the camera should also be 110° FOV.  
*Note: There are 2 versions of MLX90640, being the 55° FOV version and the 110° FOV version.*

## [2] Python Programs (Python3 only)

### [2-1] 1_mlx90640.py
This program shows a live thermal imaging video read from the MLX90640.
On the upper left corner shows the minimum temperature, maximum temperature, and the current FPS.    
![alt text](https://github.com/xyth0rn/ThermalFaceDetection/blob/main/photos/thermal_image.png)

### [2-2] 2_cam_overlay_mlx.py
This program overlays the live thermal imaging video on top of the live camera.  
*Note: If the FOV of your camera does not match perfectly with the MLX90640, you can use this program to check the difference.*  
![alt text](https://github.com/xyth0rn/ThermalFaceDetection/blob/main/photos/face_thermal_overlap.png)

### [2-3] 3_thermalFaceDetection_1.py
This is the simplest thermal face detection program. The program uses jetson.inference and Facenet-120 for face detection.  
One key point in this program is the resolution setting. The resolution of MLX90640 is 4:3, while the resolution of the `jetson.utils.videoSource("csi://0")` is 16:9. In order to match the resolution of the two video sources, it is necessary to trim the video input of the MLX90640 from 4:3 to 16:9. This can be achieved by using the `numpy.reshape()` function.  
*Note: More information about the jetson.inference and Facenet-120 can be found on https://github.com/dusty-nv/jetson-inference.*  
![alt text](https://github.com/xyth0rn/ThermalFaceDetection/blob/main/photos/face_detection.png)

### [2-4] 4_thermalFaceDetection_2.py
This model is based on the Single-Shot-Multibox detector and ResNet-10 Architecture as the backbone. The program uses the `cv2.dnn` module to do inference.  
It is worth noting that the resolution of this program's output is 4:3, meaning that this program uses the whole thermal imaging video source by MLX90640, thus granting the program a higher accuracy in thermal detection. 

*Note: the `cv2.dnn` module is based on the Single-Shot-Multibox detector and uses ResNet-10 Architecture as the backbone. More detailed information can be found at https://learnopencv.com/face-detection-opencv-dlib-and-deep-learning-c-python/ and https://www.pyimagesearch.com/2018/02/26/face-detection-with-opencv-and-deep-learning/.*

*Note: OpenCV 4.5 version or later is needed in order to use CUDA. More information about installing OpenCV 4.5 can be found at https://qengineering.eu/install-opencv-4.5-on-jetson-nano.html.*

![alt text](https://github.com/xyth0rn/ThermalFaceDetection/blob/main/photos/face_temperature.png)

### [2-5] 5_thermalFaceDetection_3.py
Thermal face detection with Haar cascades model.

## [4] Improvements
After some testing, I noticed that the accuracy of the thermal sensor declines as the distance between a person and the device increases. I have thought about a possible solution but it has not been tested. By adding an ultrasonic sensor to the device, I believe it is possible to achieve further calibration between the distance and the temperature results.

## [5] Youtube Link  
Low Cost Thermal Face Detection Device with Nvidia Jetson Nano and MLX90640  
https://youtu.be/hpyW4LwhL44  

## [6] Reference
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

Q-engineering: Install OpenCV 4.5 on Jetson Nano  
https://qengineering.eu/install-opencv-4.5-on-jetson-nano.html
