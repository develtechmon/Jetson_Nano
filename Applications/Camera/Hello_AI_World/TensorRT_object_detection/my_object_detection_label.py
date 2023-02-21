#!/usr/bin/python3

import jetson.inference
import jetson.utils

net = jetson.inference.detectNet("SSD-Mobilenet-v2", threshold=0.5)
camera = jetson.utils.videoSource("csi://0")      # '/dev/video0' for V4L2
#camera = jetson.utils.videoSource("/dev/video0") #for V4L2
display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file

while display.IsStreaming():
	img = camera.Capture()
	detections = net.Detect(img)
	#print(detections[0].ClassID)
	for detection in detections:
		label = net.GetClassDesc(detection.ClassID)
		print(label)
	display.Render(img)
	display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
