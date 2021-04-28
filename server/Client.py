import numpy as np

class Client:

    """
    This class holds the information about a client connected to the API.
    """

    frames = []
    lastAnalysedTime = 10000
    browser_id = 0
    savedOutput = np.zeros((300, 300, 3))
    solved = False
    reAnalyse = True

    def __init__(self, browser_id):
        self.browser_id = browser_id

    def registerFrame(self, frame_id):
        self.frames.append(int(frame_id))
    
    def deregisterFrame(self, frame_id):
        self.frames.remove(int(frame_id))

    def next(self):
        nextFrame = min(self.frames)
        return nextFrame