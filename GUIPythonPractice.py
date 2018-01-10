from tkinter import *
import _thread
import time
import numpy as np
import cv2

#Default colors for filter, later to be changed by GUI
filterColorLow = [0,120,154]
filterColorHigh = [255,255,255]

def imageProcess():

	#Create video stream from camera (0) for laptop webcam, (1) for usb webcam. On a desktop probably (0) for a USB webcam
	cap = cv2.VideoCapture(0)


	frame_width = int(cap.get(3))#cv2.CV_CAP_PROP_FRAME_WIDTH)) 3
	frame_height = int(cap.get(4))#cv2.CV_CAP_PROP_FRAME_HEIGHT)) 4

	#create video file to write to.
	out = cv2.VideoWriter('video.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

	fileIndex = 0
	frameState = 0
	while(True):
	    # Capture frame-by-frame
	    ret, frame = cap.read()

	    frame = cv2.flip(frame,1)
	    frame = cv2.imread('stopsign.jpg',1)
	    #out.write(frame)

	    # Our operations on the frame come here
	    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	    #hsv = frame

	    #Colors to filter between
	    lower_red = np.array(filterColorLow)
	    upper_red = np.array(filterColorHigh)
	    

	    #Create a filter to apply to an image
	    mask = cv2.inRange(hsv, lower_red, upper_red)
	    #Apply the filter to the image
	    filteredFrame = cv2.bitwise_and(frame,frame, mask= mask)
	    #cv2.putText(filteredFrame,str(lower_red), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)

	    # Display the resulting frames
	    if (frameState == 0):
	        cv2.imshow('Frame',frame)
	    elif (frameState == 1):
	        cv2.imshow('HSV',hsv)
	    elif (frameState == 2):
	        cv2.imshow('Mask',mask)
	    elif (frameState == 3):
	        cv2.imshow('Filter',filteredFrame)
	    

	    #Read input from the keyboard
	    key = cv2.waitKey(1)
	    if (key == ord('s')):
	    	fileIndex += 1
	    	fileName = 'pic' + str(fileIndex) + ".bmp"
	    	cv2.imwrite(fileName,frame)
	    if (key == ord('n')):
	            frameState = (frameState + 1) % 4
	            cv2.destroyAllWindows()
	    if (key == ord('q')):
	        break

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()



top = Tk()
texts = ["R","G","B","R","G","B"]
labels = []
inputs = []
for i in range(6):
	label = Label(top, text = texts[i])
	label.grid(row = i)
	labels.append(label)
	input_ = Scale(top, from_=0, to=255,orient = HORIZONTAL)
	input_.grid(row = i, column = 1)
	inputs.append(input_)

# redLabel = tkinter.Label(top, text="R:")
# redLabel.grid(row = 0)
# redInput = tkinter.Scale(top, from_=0, to=100,orient = tkinter.HORIZONTAL) #tkinter.Entry(top, bd =5)
# redInput.grid(row = 0, column = 1)

# greenLabel = tkinter.Label(top, text="G:")
# greenLabel.grid(row = 1)
# greenInput = tkinter.Entry(top, bd =5)
# greenInput.grid(row = 1, column = 1)

# blueLabel = tkinter.Label(top, text="B:")
# blueLabel.grid(row = 2)
# blueInput = tkinter.Entry(top, bd =5)
# blueInput.grid(row = 2, column = 1)

def updateColors():
	for i in range(3):
		filterColorLow[i] = inputs[i].get()
		filterColorHigh[i] = inputs[i+3].get()
	print(filterColorLow)
	print(filterColorHigh)

button = Button(top, text ="Update", command = updateColors)
button.grid(row = len(labels), column = 1)

_thread.start_new_thread(imageProcess,())

top.mainloop()


