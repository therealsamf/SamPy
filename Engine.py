
#Engine.py

print("Name = " + __name__)

print("Running Engine Module")

import os, sys

#print(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if (__name__ == "SamPy.Engine"):
#    try:
        from . import Log
        from . import Event
        from . import Resource
        from . import Renderer
        from . import GameLogic
#    except:
#        print("Unable to import modules")

else:
    import Log
    
global DebugMode

class Engine():
    gEngine = None
    def __init__(self):
        self._log = None
        self._eventManager = None
        self._gameLogic = None
        self._resourceCache = None
        self._scriptManager = None

        if (Engine.gEngine == None):
            Engine.gEngine = self

    #Initializes the engine and all subsystems
    def Initialize(self):

        #Initialize the Log first, so that we can start logging

        self.Log = Log.Log()
        if (not self.Log.Initialize()):
            print("Log file failed to initialize!") #Use print logging because
            #real logging wasn't successfully initialized
            return #We don't want to do anything else while the log hasn't
        #initialized
        Log.LogMessage("Initializing SamPy")
        Log.LogMessage("Initialized Log")

        
        self.EventManager = Event.EventManager.EventManager();
        if (not self.EventManager.Initialize()):
            Log.LogError("EventManager failed to initialize!")
            return
 
        self.ResourceCache = Resource.ResourceCache.ResourceCache()
        if (not self.ResourceCache.Initialize()):
            Log.LogError("ResourceCache failed to initialize!")
            return

    def SetAndRunGameLogic(self, gameL):
        self.GameLogic = gameL
        if not self.GameLogic.Initialize():
            Log.LogError("Failure to initialize GameLogic!")
            return
        eType = Event.Event.GetType('EngineInitialized')
        self.EventManager.TriggerEvent(Event.Event.Event(eType, EngineInitializedData()))
    
        self.GameLogic.run()

    def SetGameLogic(self, gameL):
        self.GameLogic = gameL
        if not self.GameLogic.Initialize():
            Log.LogError("Failure to intialize GameLogic!")
            return
        eType = Event.Event.GetType('EngineInitialized')
        self.EventManager.TriggerEvent(
            Event.Event.Event(eType, EngineInitializedData()))
        
        
                
    @property
    def EventManager(self):
        return self._eventManager

    @EventManager.setter
    def EventManager(self, value):
        self._eventManager = value

    @property
    def Log(self):
        return self._log

    @Log.setter
    def Log(self, value):
        self._log = value

    @property
    def GameLogic(self):
        return self._gameLogic

    @GameLogic.setter
    def GameLogic(self, value):
        self._gameLogic = value

    @property
    def ScriptManager(self):
        return self._scriptManager
"""
    @ScriptManager.setter
    def ScriptManager(self, value):
        self._scriptManaget = value
"""
DebugMode = True

class EngineInitializedData(Event.Event.EventData):
    def __init__(self):
        super().__init__()
