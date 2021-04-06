import numpy as np

class Client:

    frames = []
    lastClassificationTime = 10000
    browser_id = 0
    savedOutput = np.zeros((300, 300, 3))
    solved = False
    reclassify = True

    def __init__(self, browser_id):
        self.browser_id = browser_id

    def registerFrame(self, frame_id):
        print(self.frames, "registering ", "frame_id: ", frame_id, " from client with browser_id: ", self.browser_id)
        self.frames.append(int(frame_id))
    
    def deregisterFrame(self, frame_id):
        print(self.frames, "removing ", "frame_id: ", frame_id, " from client with browser_id: ", self.browser_id)
        self.frames.remove(int(frame_id))

    def isNext(self, frame_id):
        nextFrame = min(self.frames)
        print("next is: ", "frame_id: ", nextFrame, " from client with browser_id: ", self.browser_id)
        try:
            return int(frame_id) == nextFrame
        except:
            return True

    def purgeBefore(self, frame_id):
        print(self.frames)
        tempFrames = self.frames
        for i in self.frames:
            if i < frame_id:
                tempFrames.remove(i)
        self.frames = tempFrames