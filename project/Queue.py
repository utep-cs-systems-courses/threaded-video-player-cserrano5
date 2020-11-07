
import cv2, os, sys
from threading import Thread, Semaphore, Lock

#queue class for frames
class Queue():
    
    def __init__(self,cap = 10):       #set cap for queue to 10, can be changed
       self.queue = []                 #create list
       self.qLock = Lock()             #lock
       self.full = Semaphore(0)        #counts to see if lock is full, starts at 0
       self.empty = Semaphore(cap)     #counts to see if lock is empty, starts sat cap

    def put(self,frame):
        self.empty.acquire()           #aquire from empty
        self.qLock.acquire()           #aquire lock
        self.queue.append(frame)       #append queue
        self.qLock.release()           #release lock
        self.full.release()            #release from full

    def get(self):
        self.full.acquire()            #aquire from full
        self.qLock.acquire()           #aquire lock
        frame = self.queue.pop(0)      #pop first element from queue
        self.qLock.release()           #release lock
        self.empty.release()           #release from empty
        return frame                   #returns frame
