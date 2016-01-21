#ProcessManager.py

from . import Process
from .. import Log

class ProcessManager():
    gProcessManager = None
    def __init__(self):
        self._activeProcesses = None
        self._deadProcess = None
        self._lastUpdate = None
        if (ProcessManager.gProcessManager == None):
            ProcessManager.gProcessManager = self
        else:
            Log.LogError("Attempting to create two global ProcessManagers!")

    def Initialize(self):
        Log.LogMessage("Initializing Process Manager")
        self._lastUpdate = 0
        self._activeProcesses = list()
        return True

    def AttachProcess(self, process):
        process.State = Process.ALIVE
        self._activeProcesses.append(process)
        Log.LogMessage("Attaching Process " + process.toString() + " to active processes")

    def UpdateProcesses(self, deltaMilliseconds):
        successCount = 0
        failureCount = 0
        #Reverse and traverse list backwards, enables me to remove
        #dead processes from the list as I traverse it
        self._activeProcesses.reverse()
        index = len(self._activeProcesses) - 1
        while (index >= 0):
            process = self._activeProcesses[index]
            process.Update(deltaMilliseconds)
            if (process.IsDead()):
                self._activeProcess.pop(index)
                if (process.State == Process.SUCCEEDED):
                    process.OnSucceed()
                    successCount += 1
                elif (process.State == Process.FAILED):
                    process.OnFail()
                    failureCount += 1
                elif (process.State == Process.ABORTED):
                    process.OnAbort()
                    failureCount += 1 #? I don't know if I should be increasing failure for aborted processes or not

            index -= 1


        return successCount, failureCount

    def AbortAll(self):
        for process in self._activeProcesses:
            process.State = Process.Abort()

    def RemoveProcess(self, process):
        self._activeProcesses.remove(process)

    def RemoveAll(self):
        while (len(self._activeProcesses) > 0):
            self._activeProcesses.pop()


    
            

        
        
