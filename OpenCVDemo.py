import numpy as np
import cv2
import tkinter
from time import sleep

def changeFilter(display):
    R = redInput.get()
    G = greenInput.get()
    B = blueInput.get()
    display.text.set(R + " " + G + " " + B)


top = tkinter.Tk()
frame = tkinter.Frame(top,width = 100,height = 100)
redLabel = tkinter.Label(frame, text="R:")
redLabel.grid(row = 0)
redInput = tkinter.Entry(frame, bd =5)
redInput.grid(row = 0, column = 1)

greenLabel = tkinter.Label(frame, text="G:")
greenLabel.grid(row = 1)
greenInput = tkinter.Entry(frame, bd =5)
greenInput.grid(row = 1, column = 1)

blueLabel = tkinter.Label(frame, text="B:")
blueLabel.grid(row = 2)
blueInput = tkinter.Entry(frame, bd =5)
blueInput.grid(row = 2, column = 1)

display = tkinter.Label(frame, text="No input")
display.grid(row = 4)

applyFilterButton = tkinter.Button(frame, text='OK', command=changeFilter(display))
applyFilterButton.grid(row = 3)


frame.pack()

top.mainloop()

#Create video stream from camera 
cap = cv2.VideoCapture(1)


frame_width = int(cap.get(3))#cv2.CV_CAP_PROP_FRAME_WIDTH)) 3
frame_height = int(cap.get(4))#cv2.CV_CAP_PROP_FRAME_HEIGHT)) 4

#create video file to write to.
out = cv2.VideoWriter('video.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

fileIndex = 0
frameState = 0
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    #frame = cv2.flip(frame,1)

    out.write(frame)

    # Our operations on the frame come here
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Colors to filter between
    lower_red = np.array([150,0,0])
    upper_red = np.array([255,255,255])
    

    #Create a filter to apply to an image
    mask = cv2.inRange(hsv, lower_red, upper_red)
    #Apply the filter to the image
    filteredFrame = cv2.bitwise_and(frame,frame, mask= mask)

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