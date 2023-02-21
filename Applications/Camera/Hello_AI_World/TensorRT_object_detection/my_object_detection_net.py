#!/usr/bin/python3

import jetson.inference
import jetson.utils

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box, labels, conf")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use")

try:
    opt = parser.parse_known_args()[0]
except:
    print("")
    parser.print_help()
    sys.exit(0)

# Load the object detection network
net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)

# Create video sources & outputs
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv)

# Process Frames until the user exits
while True:
    img = input.Capture()
    detections = net.Detect(img, overlay=opt.overlay)
    print("detected {:d} objects in image".format(len(detections)))

    for detection in detections:
        print(detection)
        class_desc = net.GetClassDesc(detection.ClassID)
        widths = detection.Width
        height = detection.Height
        location = detection.Center
        print("Class Description :" + class_desc + " " + "widths :" + " " + str(widths) + " " + "Height :" + str(height) + " " + "location :" + str(location) )

    output.Render(img)
    output.SetStatus("{:s} | Network {:.0f} FPS".format(opt.network, net.GetNetworkFPS()))
    net.PrintProfilerTimes()
    if not input.IsStreaming() or not output.IsStreaming():
        break

