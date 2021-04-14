class Frame:

    """
    This class holds the original image and steps of analysis for a frame
    """

    border = None
    calculated = False
    solutionFrame = False
    combinedDigits = None
    digits = None
    startTime = 0
    endTime = 0

    def __init__(self, img, frame_id):
        self.img = img
        self.frame_id = frame_id

    def timeTaken(self):
        return self.endTime - self.startTime
