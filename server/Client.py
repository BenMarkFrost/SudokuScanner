import numpy as np

class Client:

    frames = []
    lastClassificationTime = 10000
    browser_id = 0
    savedOutput = np.zeros((300, 300, 3))
    solved = False

    def __init__(self, browser_id):
        self.browser_id = browser_id

    def registerFrame(self, frame_id):
        print("registering : ", self.frames, frame_id, self.browser_id)
        self.frames.append(frame_id)
    
    def deregisterFrame(self, frame_id):
        print("removing: ", self.frames, frame_id, self.browser_id)
        self.frames.remove(frame_id)

    def isNext(self, frame_id):
        print("next is: ", min(self.frames), self.browser_id)
        try:
            return frame_id == min(self.frames)
        except:
            return True

    def purgeBefore(self, frame_id):
        print(self.frames)
        tempFrames = self.frames
        for i in self.frames:
            if i < frame_id:
                tempFrames.remove(i)
        self.frames = tempFrames