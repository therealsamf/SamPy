#Process.py

from .. import Log

#Process States
DEAD = 0
ALIVE = 1

#Process Outcomes
ABORTED = 0
FAILED = 1
SUCCEEDED = 2

class Process():
    def __init__(self):
        self._state = None
        self._child = None


    def Init(self):
        self._state = DEAD

    @property
    def State(self):
        return self._state

    @State.setter
    def State(self, value):
        #Log.LogMessage()
        self._state = value

    @property
    def Child(self):
        return self._child

    @Child.setter
    def Child(self, value):
        if isinstance(value, Process):
            self._child = value
        
    def Succeed(self):
        self._state = SUCCEEDED

    def Fail(self):
        self._state = FAILED
    def Abort(self):
        self._state = ABORTED

    #These methods are meant to be overridden
    def toString(self):
        return "base_Process"
    def OnFail(self):
        self.State = DEAD

    def OnSucceed(self):
        self.State = DEAD

    def OnAbort(self):
        self.State = DEAD

    def Update(self, deltaMilliseconds):
        pass

    def IsAlive(self):
        return self._state == ALIVE
    
    def IsDead(self):
        return self._state == DEAD

