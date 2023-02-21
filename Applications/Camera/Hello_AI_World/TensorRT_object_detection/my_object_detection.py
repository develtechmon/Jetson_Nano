#!/usr/bin/python3
import jetson.inference
import jetson.utils

net = jetson.inference.detectNet("SSD-Mobilenet-v2", threshold=0.5)
camera = jetson.utils.gstCamera(640,480, "/dev/video0")
display = jetson.utils.glDisplay()

while display.IsOpen():
    img, width, height = camera.CaptureRGBA()
    detections = net.Detect(img, width, height)
    display.RenderOnce(img, width, height)
    display.SetTitle("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
    
