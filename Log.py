#Log.py

#print("Log name: " + __name__)


import time

class Log():
    gLog = None
    Debug = None
    def __init__(self):
        self._filename = None
        self._file = None

        if (Log.gLog == None):
            Log.gLog = self
        

    def Initialize(self):
        #Gets the time and sets the filename
        timeStruct = time.localtime()
        hour = timeStruct[3]
        min = timeStruct[4]

        fileNameSequence = ("Log", str(hour), str(min))

        tempFilename = "_".join(fileNameSequence)
        self.Filename = tempFilename + ".log"

        self._file = open(self.Filename, "w")
        if (self._file == None):
            #File opening failed, print failure
            print("Failure to create/open new log file: " + self.Filename)
            return False

        return True
        
    @property
    def Filename(self):
        return self._filename

    @Filename.setter
    def Filename(self, value):
        self._filename = value

    @property
    def File(self):
        return self._file

    def log(self, msg, tag="Default"):
        if (self._file == None):
            return

        logSequence = ("[", tag, "]: ", msg, "\n")
        #construct the message to be logged
        logMsg = "".join(logSequence)
        self._file.write(logMsg)
        self._file.flush()
        return

    def __del__(self):
        if (self._file != None):
            if (not self._file.closed):
                self._file.close()


    
def LogError(msg):
    if (Log.Debug == None):
        print("Debug == None")
        try:
            Log.Debug = Engine.DebugMode
        except UnboundLocalError:
            if (__name__ == "SamPy.Log"):
                from . import Engine
                Log.Debug = Engine.DebugMode
            else:
                import Engine
                Log.Debug = Engine.DebugMode
    
    if (Log.Debug):
        if (Log.gLog != None):
            Log.gLog.log(msg, "Error")

    return

def LogWarning(msg):
    if (Log.Debug == None):
        print("Debug == None")
        try:
            Log.Debug = Engine.DebugMode
        except NameError:
            if (__name__ == "PythonGameEngine.Log"):
                from . import Engine
                Log.Debug = Engine.DebugMode
            else:
                import Engine
                Log.Debug = Engine.DebugMode
    
    if (Log.Debug):
        if (Log.gLog != None):
            Log.gLog.log(msg, "Warning")

    return

def LogMessage(msg, tag="Default"):
    if (Log.Debug == None):
        #print("Debug == None")
        try:
            Log.Debug = Engine.DebugMode
        except (NameError, UnboundLocalError):
            if (__name__ == "SamPy.Log"):
                from . import Engine
                Log.Debug = Engine.DebugMode
            else:
                import Engine
                Log.Debug = Engine.DebugMode
                
    if (Log.Debug):
        if (Log.gLog != None):
            Log.gLog.log(msg, tag)
    return
