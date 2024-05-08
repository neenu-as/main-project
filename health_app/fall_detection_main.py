# USAGE
# python yolo_video.py --input videos/airport.mp4 --output output/airport_output.avi --yolo yolo-coco

# import the necessary packages
import numpy as np

import time
import cv2
import os
# from src.dbconnection import *
import requests
from django.core.files.storage import FileSystemStorage

from health_app.recognize_face import rec_face_image

labelsPath = os.path.sep.join(["C:\\Users\\Neenu as\\Desktop\\PROJECT\\HealthMonitoringSystem\\static\\yolo-coco", "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# initialize a list of colors to represent each possible class label
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")

# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join(["C:\\Users\\Neenu as\\Desktop\\PROJECT\\HealthMonitoringSystem\\static\\yolo-coco", "yolov3.weights"])
configPath = os.path.sep.join(["C:\\Users\\Neenu as\\Desktop\\PROJECT\\HealthMonitoringSystem\\static\\yolo-coco", "yolov3.cfg"])

# load our YOLO object detector trained on COCO dataset (80 classes)
# and determine only the *output* layer names that we need from YOLO
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# initialize the video stream, pointer to output video file, and
# frame dimensions
# r"G:\yolo\yolo-object-detection\videos\airport.mp4"
# vs = cv2.VideoCapture(0)
# vs = cv2.VideoCapture("C:\\Users\\Neenu as\\Desktop\\PROJECT\\HealthMonitoringSystem\\static\\arundhadhi.mp4")
vs = cv2.VideoCapture("C:\\Users\\Neenu as\\Desktop\\PROJECT\\HealthMonitoringSystem\\static\\velli.mp4")
# vs = cv2.VideoCapture("C:\\Users\\Neenu as\\Desktop\\PROJECT\\HealthMonitoringSystem\\static\\queda.mp4")
writer = None
(W, H) = (None, None)



# loop over frames from the video file

listop=[]
listra=[]
counti=0
ress=[]
flag=False
while True:
	if len(listop)==20:
		listop=listop[1:]
		listra=listra[1:]
	counti=counti+1
	# read the next frame from the file

	(grabbed, frame) = vs.read()
	_, frame = vs.read()

	print("==> ",counti)
	# if the frame was not grabbed, then we have reached the end
	# of the stream
	if not grabbed:
		break

	# if the frame dimensions are empty, grab them
	if W is None or H is None:
		(H, W) = frame.shape[:2]

	# construct a blob from the input frame and then perform a forward
	# pass of the YOLO object detector, giving us our bounding boxes
	# and associated probabilities
	blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),swapRB=True, crop=False)
	net.setInput(blob)
	start = time.time()
	layerOutputs = net.forward(ln)
	end = time.time()

	ret, img = vs.read()




	if len(ress)>0:

		pass
	else:
		cv2.imwrite("a.jpg", img)
		ress = rec_face_image("C:\\Users\\Neenu as\\Desktop\\PROJECT\\HealthMonitoringSystem\\health_app\\a.jpg")
		print(ress, "======================================result")

	# initialize our lists of detected bounding boxes, confidences,
	# and class IDs, respectively
	boxes = []
	confidences = []
	classIDs = []

	# loop over each of the layer outputs
	for output in layerOutputs:
		# loop over each of the detections
		for detection in output:
			# extract the class ID and confidence (i.e., probability)
			# of the current object detection
			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]

			# filter out weak predictions by ensuring the detected
			# probability is greater than the minimum probability
			if confidence > 0.5 and classID==0:
				# print("==============================abnormality detected")
				# scale the bounding box coordinates back relative to
				# the size of the image, keeping in mind that YOLO
				# actually returns the center (x, y)-coordinates of
				# the bounding box followed by the boxes' width and
				# height
				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")

				# use the center (x, y)-coordinates to derive the top
				# and and left corner of the bounding box
				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))

				# update our list of bounding box coordinates,
				# confidences, and class IDs
				boxes.append([x, y, int(width), int(height)])
				confidences.append(float(confidence))
				classIDs.append(classID)

	# apply non-maxima suppression to suppress weak, overlapping
	# bounding boxes
	idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.4,
		0.5)


	# ensure at least one detection exists
	if len(idxs) > 0:
		# loop over the indexes we are keeping
		for i in idxs.flatten():
			# extract the bounding box coordinates
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])

			# draw a bounding box rectangle and label on the frame
			color = [int(c) for c in COLORS[classIDs[i]]]
			cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
			text = "{}: {:.4f}".format(LABELS[classIDs[i]],
				confidences[i])
			if LABELS[classIDs[i]]=="person":
				cv2.putText(frame, text, (x, y - 5),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
				ra=w/h
				if w>h:
					if len(listop)==0:
						flag=True
					listop.append(1)
					listra.append(ra)
				else:
					listop.append(0)
					listra.append(ra)
				break
		else:
			listop.append(0)
			listra.append(0)
	else:
		listop.append(0)
		listra.append(0)
	if listop[-1]==1:
		print(listop)
		print(listra)
		l=len(listop)
		c=0
		for i in range(2,8):
			if i<l:
				print(listra[l-i],"====================")
				if listra[l-i]>0.75:
					c=c+1
			else:
				break
		print(c,"+++++++++++++++++++++++++++++++++++++++++++++")
		print(c,"+++++++++++++++++++++++++++++++++++++++++++++")
		if c<5 and c>1:
			# qry = "INSERT INTO `fallnotification` VALUES(NULL,%s,NOW(),'pending')"

			ip="192.168.29.229"

			# ip="192.168.43.229"
			# fs=FileSystemStorage()
			# fn=fs.save("abc.jpg",img)


			print("fall detected",ress)
			print("fall detected",ress)
			print("fall detected",ress)
			print("fall detected",ress)
			print("fall detected",ress)
			print("fall detected",ress)

			import time

			ret, img2 = vs.read()

			if len(ress) > 0 and not flag:

				timestr = time.strftime("%Y%m%d-%H%M%S")

				cv2.imwrite("C:\\Users\\Neenu as\\Desktop\\PROJECT\\HealthMonitoringSystem\\media\\" + timestr + ".jpg",
							img2)
				fn = timestr + ".jpg"
				qrr2 = requests.get(
					"http://" + ip + ":5000/fall_detecion?pid=" + str(ress[0]) + "&fn=" + fn + "&cam=4&con=fall")
			else:
				pass


		elif c<9 and c>5:
			timestr = time.strftime("%Y%m%d-%H%M%S")
			cv2.imwrite("C:\\Users\\Neenu as\\Desktop\\PROJECT\\HealthMonitoringSystem\\media\\" + timestr + ".jpg",
						img2)
			fn = timestr + ".jpg"
			qrr2 = requests.get(
				"http://" + ip + ":5000/fall_detecion?pid=" + str(ress[0]) + "&fn=" + fn + "&cam=4&con=abnormal")
			print("===================================abnoraml detected.............")
			# iud(qry, 3)
	cv2.imshow('video', frame)
	if cv2.waitKey(33) == 27:
		break
# release the file pointers
print("[INFO] cleaning up...")

vs.release()