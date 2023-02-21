#!/usr/bin/python3

import jetson.inference
import jetson.utils
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="googlenet", help="pre-trained model to load")

try:
    opt = parser.parse_known_args()[0]
except:
    print("")
    parser.print_help()
    sys.exit(0)

# Load the recognition network
net = jetson.inference.imageNet(opt.network, sys.argv)

# Create video sources & outputs
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv)
font = jetson.utils.cudaFont()

while True:
    # capture the next image
    img = input.Capture()

    # classify the image
    class_id, confidence = net.Classify(img)

    # find the object description
    class_desc = net.GetClassDesc(class_id)

    # overlay the result on the image
    font.OverlayText(img, img.width, img.height, "{:05.2f}% {:s}". format(confidence * 100, class_desc), 5, 5, font.White, font.Gray40)

    # render the image
    output.Render(img)

    # update the title bar
    output.SetStatus("{:s} | Network {:.0f} FPS".format(net.GetNetworkName(), net.GetNetworkFPS()))

    # exit on input/output EOS
    if not input.IsStreaming() or not output.IsStreaming():
        break
    

