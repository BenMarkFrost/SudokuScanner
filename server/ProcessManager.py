from multiprocessing import Pool, Manager
from server.Frame import Frame
from server.Client import Client
from server import sudokuscanner
from server import digitfinder


class ProcessManager:

    # manager = Manager()
    clientsDict = {}
    finishedFrames = {}

    def __init__(self, numProcesses):
        self.pool = Pool(processes=numProcesses)
    
    def startAnalysis(self, browser_id, img, frame_id):
        try:
            client = self.clientsDict[browser_id]
        except:
            client = Client(browser_id)
            self.clientsDict[browser_id] = client
            print(f'New client: {browser_id}')

        frame = Frame(img, frame_id)
        
        # Frames are registered to their client during execution to keep track of them.
        client.registerFrame(frame.frame_id)

        # print("Sending frame to pool")
        self.pool.apply_async(sudokuscanner.scan, args=(frame, client, ), callback=self.frameFinished)
    
    def startSudokuSolve(self, frame, client):
        # print("Starting hard solve")
        client.lastAnalysedTime = digitfinder.current_milli_time()
        self.pool.apply_async(sudokuscanner.analyseFrame, args=(frame, client), callback=self.sudokuSolveFinished)

    def sudokuSolveFinished(self, client):
        newestClient = self.clientsDict[client.browser_id]
        if newestClient.solved == False or client.solved == True:
            self.clientsDict[client.browser_id] = client


    def frameFinished(self, frame):
        # print("Frame finished")
        client = self.clientsDict[frame.browser_id]
        sudokuscanner.frameBuffer(frame, client)
        client.deregisterFrame(frame.frame_id)
        self.finishedFrames[frame.frame_id] = frame
        if frame.solutionFrame:
            self.startSudokuSolve(frame, client)

    def getFrame(self, frame_id):
        frame = self.finishedFrames[frame_id]
        del self.finishedFrames[frame_id]
        return frame