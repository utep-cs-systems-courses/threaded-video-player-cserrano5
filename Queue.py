
import cv2, os, sys, time
from threading import Thread, Semaphore, Lock

#queue class for frames
class Queue():
    
    def __init__(self):      
       self.queue = []        #creates/initialize list
       self.first = Semaphore(10)             
       self.second = Semaphore(0)        
       self.mutex = Lock 

    def put(self, frame):
        self.first.acquire()          
        self.mutex.acquire()          
        self.queue.append(frame)       
        self.mutex.release()          
        self.second.release()           
        return

    def get(self):
        self.second.acquire()           
        self.mutex.acquire()          
        frame = self.queue.pop(0)      #pop first element from queue
        self.mutex.release()           #release lock
        self.first.release()          
        return frame                   #returns frame
