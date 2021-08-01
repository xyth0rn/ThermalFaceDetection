# ThermalFaceDetection

## [1] MLX90640 setup

### [1-1] install Jetson.GPIO
# https://github.com/NVIDIA/jetson-gpio
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

Final Results
![alt text](https://github.com/NicoIsAwesome/ThermalFaceDetection/blob/main/pcb_4.jpeg)
![alt text](https://github.com/NicoIsAwesome/ThermalFaceDetection/blob/main/pcb_5.jpeg)
