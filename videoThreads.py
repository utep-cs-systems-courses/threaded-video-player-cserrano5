#!/usr/bin/env python3

import cv2, os, sys, time
from Queue import Queue
import numpy as np
from threading import Thread, Semaphore, Lock




#create queues
frameQueue = Queue() 
grayQueue = Queue() 




#extracting frame thread class
class ExtractFramesThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.videocap = cv2.VideoCapture('clip.mp4')                            #this opens video clip
        self.totalFrames = int(self.videocap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.count = 0

    def run(self):                                                          #this runs code
        success, image = self.videocap.read()                                 #this reads first frame
        while True:
            if success:
                frameQueue.put(image) #gets frame
                success, image = self.videocap.read()
                print(f'Reading frame {self.count}')
                self.count = self.count + 1
                
            if self.count == self.totalFrames:
                frameQueue.put(-1)
                break
            
        print('Extraction is complete.')
      

#convert to gray scale thread class
class ConvertToGrayScaleThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.count = 0

    def run(self):                                                          #this runs code
        while True:
            frame = frameQueue.get()
            if type(frame) == int and frame == -1:
                grayQueue.put(-1)
                break
            grayscaleFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            grayQueue.put(grayscaleFrame)
                
            print('Gray scale convertion complete')
            return
        
        
#display frame thread class
class DisplayFrameThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.delay = 42
        self.count = 0
        

    def run(self):
        while True:
            frame = grayQueue.get()
            if type(frame) == int and frame == -1:
                break
            cv2.imshow('Video', frame)
            print(f'Displaying frame {self.count}')
            self.count = self.count + 1
            
            if cv2.waitKey(self.delay) and 0xFF == ord('q'):
                break
            
        cv2.destroyAllWindows()
        
        print('Frame display complete')  #signal threas has ended
        return
        
    
extractFrame = ExtractFramesThread()   #extract thread created
extractFrame.start()

convertGray = ConvertToGrayScaleThread()  #convert to gray thread created
convertGray.start()

displayFrame = DisplayFrameThread()    #display frame thread created
displayFrame.start()
