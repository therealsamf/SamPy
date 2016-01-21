#Event.py

#from .. import Renderer
from .. import Log

class Event():
    """This is an immutable event. Once the type and data is set, it cannot be 
changed by anybody. If data needs to be changed it would have to be done in an
 another event"""
    def __init__(self, EventType, EventData):
        self._type = EventType
        self._data = EventData


    @property
    def EventType(self):
        return self._type

    @property
    def EventData(self):
        return self._data


def enum(*sequential, **named):
    for key, value in named.items():
        named[key] = value.lower()
    nSequential = list()
    for item in sequential:
        nSequential.append(item.lower())
    sequential = tuple(nSequential)
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

EventTypes = enum('ObjectCreated', 'ObjectDestroyed', 'ObjectMoved',
                  'MouseButtonUp', 'MouseButtonDown', 'MouseMove',
                  'KeyDown', 'KeyUp', 'Quit', 'MoveCamera', 'EngineInitialized',
                  'AddUpdateRect', 'ScheduleRender'
                  )

def GetType(eType):
    try:
        eType = EventTypes.__getattribute__(EventTypes, eType.lower())
    except (AttributeError, SyntaxError):
        return None
    return eType

class EventData():
    #This class is just mean to be subclassed
    #EventData should also be immutable, none of it's fields should be able to be changed after
    #creation
    def __init__(self):
        pass

class ObjectCreatedData(EventData):
    def __init__(self, Object):
        self._objectPtr = Object

    @property
    def Object(self):
        return self._objectPtr

class ObjectDestroyedData(EventData):
    def __init__(self, Object):
        self._objectPtr = Object

    @property
    def Object(self):
        return self._objectPtr

class MouseData(EventData):
    def __init__(self, mouseEvent):
        self._x = mouseEvent.pos[0]
        self._y = mouseEvent.pos[1]
        #We need to convert these from pixel coordinates into world coordinates
        #this method is currently only found in the renderer
        from .. import Renderer
        self._coor = Renderer.Renderer.Renderer.ConvertFromPixelCoor((self._x, self._y))
        self._button = None
        self._buttons = None
        self._rel = None
        try:
            self._button = mouseEvent.button
        except AttributeError:
            self._rel = mouseEvent.rel
            self._buttons = mouseEvent.buttons

    @property
    def Buttons(self):
        return self._buttons
    @property
    def Button(self):
        return self._button
    @property
    def Rel(self):
        return self._rel
    @property
    def Coor(self):
        return self._coor

    @property
    def X(self):
        return self.Coor[0]
    @property
    def Y(self):
        return self.Coor[1]

class KeyEventData(EventData):
    def __init__(self, pygameKeyEvent):
        try:
            self._unicode = pygameKeyEvent.unicode
        except AttributeError:
            self._unicode = None
        self._key = pygameKeyEvent.key
        self._mod = pygameKeyEvent.mod

    @property
    def Key(self):
        return self._key

    @property
    def Mod(self):
        return self._mod
    @property
    def Unicode(self):
        return self._unicode
    
class QuitData(EventData):
    """There should be nothing to this event. Maybe we use this to see if the user's saved?"""
    def __init__(self):
        super().__init__() #Cas why the heck not...
        Log.LogMessage("Attempting to quit game")
