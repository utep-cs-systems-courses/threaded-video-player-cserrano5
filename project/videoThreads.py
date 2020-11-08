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

    
        
