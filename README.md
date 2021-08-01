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
circuit connection recommended by Melexis
![alt text](https://github.com/NicoIsAwesome/ThermalFaceDetection/blob/main/mlx90640_cir.png)
![alt text](https://github.com/NicoIsAwesome/ThermalFaceDetection/blob/main/mlx90640_sch.png)
![alt text](https://github.com/NicoIsAwesome/ThermalFaceDetection/blob/main/mlx90640_lay.png)
![alt text](https://github.com/NicoIsAwesome/ThermalFaceDetection/blob/main/pcb_1.jpeg)
![alt text](https://github.com/NicoIsAwesome/ThermalFaceDetection/blob/main/pcb_2.jpeg)
![alt text](https://github.com/NicoIsAwesome/ThermalFaceDetection/blob/main/pcb_3.jpeg)
![alt text](https://github.com/NicoIsAwesome/ThermalFaceDetection/blob/main/pcb_4.jpeg)
![alt text](https://github.com/NicoIsAwesome/ThermalFaceDetection/blob/main/pcb_5.jpeg)
