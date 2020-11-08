#!/usr/bin/env python3

import cv2, os, sys, time
import numpy as np
from threading import Thread, Semaphore, Lock

#global variables
clipName = 'clip.mp4'
frameQueue = []
grayQueue = []
frameCap = 50

#extracting frame thread class
class ExtractFramesThread(Thread):
    def __init__(self, semaphore):
        Thread.__init__(self)
        self.vidcap = cv2.VideoCapture(clipName)                            #this opens video clip
        self.vidlen = int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT))-1      #videos max frames
        self.queuecap = frameCap                    #frames to extract before moving to next thread
        self.count = 0                                                      #counts frames done
        self.semaphore = semaphore                                          #lock

    def run(self):                                                          #this runs code
        success, image = self.vidcap.read()                                 #this reads first frame
        while True:
            self.semaphore.acquire()                                        #lock
            if success and len(frameQueue) <= self.queuecap: #checks frame was read & queue notfull
                print(f'Reading frame {self.count}')
                frameQueue.append(image)                     #append to frame queue
                success, image = self.vidcap.read()          #reads next frame
                self.count = self.count + 1                  #increases count
            self.semaphore.release()                         #release

            if self.count == self.vidlen:                    #if count equals the max frames, done
                print('Extracting is done.')
                break
        return

    
        
#convert to gray scale thread class
class ConvertToGrayScaleThread(Thread):
    def __init__(self, semaphore):
        Thread.__init__(self)
        self.vidcap = cv2.VideoCapture(clipName)                            #this opens video clip
        self.vidlen = int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT))-1      #videos max frames
        self.queuecap = framecap                   #frame to extract before moving to next thread
        self.count = 0                                                      #counts frames done
        self.semaphore = semaphore                                          #lock

    def run(self):                                                          #this runs code
        while True:
            self.semaphore.acquire()                                        #lock
            if frameQueue and len(grayQueue) <= self.queuecap: #check frame was read & gray notfull
                print(f'Converting frame {self.count} to grayscale')
                inputFrame = frameQueue.pop(0)  #gets the first frame in queue
                grayScaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY) #converts to gray
                grayQueue.append(grayScaleFrame)               #appends gray queue
                self.count = self.count + 1                    #increase frame count
            self.semaphore.release()

            if self.count == self.vidlen:
                print("Converting to gray scale has been done")
                break
        return
        

#display frame thread class
class DisplayFrameThread(Thread):
    def __init__(self,semaphore):
        Thread.__init__(self)
        self.vidcap = cv2.VideoCapture(clipName)                             #this opens video clip
        self.vidlen = int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT))-1       #videos max frames
        self.delay = 42                                                 #time each frame is delayed
        self.count = 0                                                      #counts num frames done
        self.semaphore = semaphore                                           #lock

    def run(self):
        while True:
            self.semaphore.acquire()                                        #lock
            if grayQueue:
                print(f'Displaying frame {self.count}')
                inputFrame = grayQueue.pop(0)                    #pop the first frame in gray queue
                cv2.inshow('video', inputFrame)                    #displays the frame
                self.count = self.count + 1                        #increase frame count
                if cv2.waitKey(self.delay) and 0xFF == ord("q"):   #delays frame
                    break
            self.semaphore.release()

            if self.count == self.vidlen:
                print("Displaying frames has been done.")
                break
        cv2.destroyAllWindows()                                 #this closes all windows of display
        return
        
