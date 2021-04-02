class Frame:

    border = None
    calculated = False
    solutionFrame = False

    def __init__(self, img, frame_id):
        self.img = img
        self.frame_id = frame_id
