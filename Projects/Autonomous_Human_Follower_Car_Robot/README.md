# Autonomous Human Follower Car Robot using Jetson Nano

## Components Used in this project
* Jetson Nano 4gb
* Arduino Mega
* CSI Camera IMX219
* Macrinum Wheel x 4
* Switch 
* Jetson Nano UPS power supply
* Motor Driver shield v2

## Package Requirements
* CSI camera package from jetson hack for fast inference
* OpeCV - refer to https://github.com/Captluke2328/User_Guide/blob/main/Guide_Document/Installation_Guide_OpenCv_v_4_5_2
* pip install flask
* pip install pyserial

## In this project, user can run code using Flask (For webstream) or without Flask
Run flask code as follow:
> sudo python3 flask_main.py

Run non flask code as follow:
> sudo python3 main.py

