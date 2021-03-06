#EventManager.py

from .. import Log
from . import Event
from . import QuadTree
from .. import Renderer

EventTypes = Event.EventTypes
MouseButtonDown = Event.GetType('MouseButtonDown')
MouseButtonUp = Event.GetType('MouseButtonUp')
MouseMove = Event.GetType('MouseMove')

evnt = Event
ConvertFromPixelCoor = Renderer.Renderer.Renderer.ConvertFromPixelCoor
ConvertFromWorldCoor = Renderer.Renderer.Renderer.ConvertFromWorldCoor

GetGui = QuadTree.GetGui

class EventManager():
    gEventManager = None
    def __init__(self):
        if (EventManager.gEventManager == None):
            EventManager.gEventManager = self

        self._delegates = None
        self._queues = None
        self._currentQueue = 0;
        self._capturingComponent = None
        self._quadTree = None
        
    def Initialize(self):
        Log.LogMessage("Initializing EventManager")

        self._delegates = dict()
        self._queues = list()
        self._queues.append(list())
        self._queues.append(list())
        self._currentQueue = 0
        Log.LogMessage('Initializing QuadTree')
        self._quadTree = QuadTree.QuadTree()
        self._quadTree.Initialize(self)
        
        return True

    def RegisterDelegate(self, EventType, delegate):
        eType = None
        if type(EventType) == str:
            try:
                eType = Event.GetType(EventType.lower())

            except BaseException:
                Log.LogError("Type: " + EventType + " isn't defined in EventTypes!")
                return
        else:
            eType = EventType

        if eType == None:
            Log.LogError("EventType retrieval failed for type: " + \
                         str(EventType))
        if (not eType in self._delegates):
            self._delegates[eType] = set()

        eventDelegates = self._delegates[eType]
        eventDelegates.add(delegate)

    def TriggerEvent(self, Event):
        """This method skips the queue, and just calls all delegates under the event right now"""
        eType = Event.EventType
        if (eType in self._delegates):
            for delegate in self._delegates[eType]:
                delegate(eData)
    
    def Update(self):
        #Go through the events stored in the current queue,
        #call every delegate assigned to each event        
        currentQueue = self._queues[self._currentQueue]
        self._currentQueue %= 1

        empty = False
        while (not empty):
            try:
                Event = currentQueue.pop(0)

            except IndexError:
                empty = True
                break

            if (not Event.EventType in self._delegates):
                continue
            else:
                delegateList = self._delegates[Event.EventType]
                for delegate in delegateList:
                    delegate(Event.EventData)

    def QueueEvent(self, *args):
        if len(args) == 1:
            #This must be a pre-constructed event that just needs to be added to the queue
            self._queues[self._currentQueue].append(args[0])

        elif len(args) == 2:
            #This must be a type, either string or actual type, and EventData
            eType = None
            eData = None
            if (issubclass(args[0].__class__, Event.EventData)):
                eData = args[0]
                eType = args[1]
            else:
                eData = args[1]
                eType = args[0]
            if type(eType) == str:
                try:
                    eType = EventTypes.__getattrbute__(EventTypes, eType)
                except AttributeError:
                    Log.LogError("Attempting to raise an Event with a" + \
                                 " type that isn't registered!")
                    return
            event = Event.Event(eType, eData)
            self._queues[self._currentQueue].append(event)
        else:
            Log.LogError("Incompatible number of args in RaiseEvent method call!")
        return

    def Capture(self, GuiComponent):
        self._capturedComponent = GuiComponent

    def Release(self):
        self._capturedComponent = False
            
