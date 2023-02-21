#!/usr/bin/python3
import jetson.inference
import jetson.utils

net = jetson.inference.detectNet("SSD-Mobilenet-v2", threshold=0.5)
#camera = jetson.utils.gstCamera(1280,720,"/dev/video0")
camera = jetson.utils.gstCamera(1640,720,"csi://0")

display = jetson.utils.glDisplay()

while display.IsOpen():
    img, width, height = camera.CaptureRGBA()
    detections = net.Detect(img, width, height)
    for detection in detections:
        label = net.GetClassDesc(detection.ClassID)
        widths = detection.Width
        area = detection.Area
        location = detection.Center
        #print("Label:" + " " + label + " " + " Widths:" + " " + str(widths) + " " + " Area:" + " " + str(area))
        print("label :" + label + "\n" + "widths :" + str(widths) + "\n" + "area :" +  str(area) + "\n" + "center :" + str(location) + "\n")

    display.RenderOnce(img, width, height)
    display.SetTitle("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
    