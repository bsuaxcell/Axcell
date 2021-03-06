import numpy as np
import cv2

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
stop_sign = cv2.CascadeClassifier('stopsign_classifier.xml')

cap = cv2.VideoCapture(1)

while 1:
	ret, img = cap.read();
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	#gray = cv2.flip(img,1)
	#img = cv2.flip(img,1)

	stopSigns = stop_sign.detectMultiScale(gray,1.5,5)
	width = 0
	if(len(stopSigns) != 0):
		#closestStopSign = max(stopSigns,key = cv2.contourArea)
		closestStopSign = stopSigns[0]

		x,y,w,h = closestStopSign
		width = w
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
		distance = 500/w
		cv2.putText(img,str(distance), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)

	#stopSigns = None

	# for (x,y,w,h) in stopSigns:
	#     cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

	# What is 1.3 and 5
	# faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	#What are x y w an h
	# for (x,y,w,h) in faces:
	#     cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	#     roi_gray = gray[y:y+h, x:x+w]
	#     roi_color = img[y:y+h, x:x+w]
		
	#     eyes = eye_cascade.detectMultiScale(roi_gray)
	#     for (ex,ey,ew,eh) in eyes:
	#         cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

	cv2.imshow('img',img)

	k = cv2.waitKey(30) & 0xff
	if (k == ord('s')):
		fileName = 'Width' + str(width) + ".bmp"
		cv2.imwrite(fileName,img)
	if k == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()