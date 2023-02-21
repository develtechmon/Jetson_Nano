import cv2
import numpy as np

cap = cv2.VideoCapture(0)
whT = 320
confidenceThreshold = 0.5
nms_threshold = 0.3

classFiles = r'E:\Python Project\Resources\AI_Files\Yolo_v3\coco.names'
classNames = []

# --- Read the Coco name file contents---
with open(classFiles, 'rt') as f:
    classNames = f.read().rstrip('\n').rsplit('\n')
    #print(classNames)
    #print(len(classNames))

# ---Initialize the Yolo v3 names files---
modelConfiguration = r'E:\Python Project\Resources\AI_Files\Yolo_v3\yolov3-tiny.cfg'
modelWeight = r'E:\Python Project\Resources\AI_Files\Yolo_v3\yolov3-tiny.weights'


# --- Create our network ---
net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeight)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

def findObjects(outputs,img):
    hT, wT, cT = img.shape
    #print(img.shape) # 480, 640, 3
    boundingbox = []
    classIds = []
    confidenceLevel = []

    for output in outputs:
        for detect in output:
            scores = detect[5:] # Read the data from 5
            classId = np.argmax(scores) # Filter out and find the highest scores within the first 5 and takes its ID
            confidence = scores[classId] # Find the confidence by referring to highest schore ID

            if confidence > confidenceThreshold:
                w,h = int(detect[2]*wT), int(detect[3]*hT)
                x,y = int((detect[0]*wT)-w/2), int((detect[1]*hT - h/2))
                #print(w,h,x,y)
                boundingbox.append([x,y,w,h])
                classIds.append(classId)
                confidenceLevel.append(float(confidence))
    #print(len(boundingbox)) # Determine how many object it detects

    indices = cv2.dnn.NMSBoxes(boundingbox,confidenceLevel,confidenceThreshold,nms_threshold)
    for i in indices:
        i = i[0]
        box = boundingbox[i]
        x,y,w,h = box[0], box[1], box[2], box[3]
        #print(x,y,w,h)
        cv2.rectangle(img, (x, y), (x+w,y+h), (255, 0 , 255), 2)
        cv2.putText(img,f'{classNames[classIds[i]].upper()} {int(confidenceLevel[i]*100)}%',(x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
    
while True:
    success, img = cap.read()

    # ---Convert our Capture image to Blob network---
    blob = cv2.dnn.blobFromImage(img, 1/255, (whT, whT), [0,0,1],1,crop=False)
    net.setInput(blob)
    #print(blob)

    # ---Get the name of all the layer detected from webcam --
    LayerNames = net.getLayerNames()
    #print(LayerNames)

    # --- Return the index of the output Layers --
    #print(net.getUnconnectedOutLayers())

    # --- We wanted to get output layer names within the Layer Names, we -1 to  ---
    outputNames = [LayerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]
    #print(outputNames)

    outputs = net.forward(outputNames)
    #print(outputs[0][0]) # --> Printing first row [0] only 
    #print(outputs[0]) # --> Output for 300 rows (total detection in rows) & 85 columns 80 (coco list), 5 (cx,cy,w,h,confidence)
    #print(outputs[1]) # --> Output for 1200 rows (total detection in row) & 85 columns 80 (coco list), 5 (cx,cy,w,h,confidence)
    
    findObjects(outputs,img)

    cv2.imshow("Output",img)
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break


