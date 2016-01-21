#GameLogic.py

from . import Log
from . import Renderer
from . import Physics
from . import Process
from . import Object
#from . import Engine
from . import Event
from . import QuadTree

import importlib

MouseButtonEventData = Event.Event.MouseData
KeyEventData = Event.Event.KeyEventData
QuitData = Event.Event.QuitData
#Grab some variables that will be accessed frequently
MOUSEUPTYPE = Event.GetType('MouseButtonUp')
MOUSEDOWNTYPE = Event.GetType('MouseButtonDown')
MOUSEMOTIONTYPE = Event.GetType('MouseMove')
KEYUPTYPE = Event.GetType('KeyUp')
KEYDOWNTYPE = Event.GetType('KeyDown')
QUITTYPE = Event.GetType('Quit')

ObjectCreatedType = Event.GetType('ObjectCreated')

import pygame, os
from pygame.locals import *

class GameLogic():
    def __init__(self):
        self._renderer = None
        self._physics = None
        self._processManager = None
        self._objectManager = None

        """We have to import this now, else we'll get an error"""
        from . import Engine
        self._enginePointer = Engine.Engine.gEngine
        self._renderTree = None

        self._quit = False

    def Initialize(self):
        if self._enginePointer == None:
            self._enginePointer = Engine.Engine.gEngine
        Log.LogMessage("Initializing GameLogic");
        
        self._processManager = Process.ProcessManager.ProcessManager()
        if (not self._processManager.Initialize()):
            Log.LogError("ProcessManager failed to initialize!")
            return False

        self._renderer = Renderer.Renderer.Renderer(self)
        if (not self._renderer.Initialize()):
            Log.LogError("Renderer failed to initialize!")
            return False

        self._physics = Physics.Box2DPhysics.Box2DPhysics(self)
        if (not self._physics.Initialize()):
            Log.LogError("Physics failed to initialize!")
            return False

        self._objectManager = Object.ObjectManager.ObjectManager(self)
        if (not self._objectManager.Initialize()):
            Log.LogError("ObjectManager failed to initialize!")
            return False

        self._quit = False
        self._enginePointer.EventManager.RegisterDelegate(QUITTYPE, self.QuitListener)
        return True

    @property
    def QuadTree(self):
        return self._renderTree

    def AddObjectToQuadTree(self, objekt):
        comp = objekt.GetComponent('Render')
        if comp != None:
            self._renderTree.AddElement(objekt)
            
        

    def run(self):
        startTime = pygame.time.get_ticks()

        #We need to initialize all of the currently loaded objects
        self.ObjectManager.InitializeObjects()
        self._enginePointer.EventManager.Update()
        Log.LogMessage("EventManager Updated for first time")
        while not self._quit:
            currentTime = pygame.time.get_ticks()
            self.Update(currentTime - startTime)
            startTime = currentTime
        self.Shutdown()

    def Shutdown(self):
        pass

    def LoadLevel(self, absolutefilename):
        """This method looks for a TMX object in the resource cache. If it's not
there, as in the case of loading the Editor, then the game logic attempts to
load the contents of the given file itself"""
        filename = os.path.split(absolutefilename)[1]

        #Check to see if it's an actual level file
        if self._enginePointer.ResourceCache.PeekFile(filename):

            #Eventually pass everything to the object manager and stuff
            #to load the level and get this party started
            pass

        #This is something handmade like the editor's gui elements
        else:
            #Create a camera, because I probably won't include that
            #in the handmade file
            self.ObjectManager.CreateCamera()
            #Load the rest of the objects (GUI)
            self.ObjectManager.LoadObjects(absolutefilename)

            """The following line is currently hardcoded and needs to change"""
            self._renderTree = QuadTree.QuadTree((0, 0), (800, 400))
            if not self._renderTree.Initialize():
                Log.LogError("Failed to initialize GameLogic's QuadTree")
            
    @property
    def Renderer(self):
        return self._renderer

    @property
    def ProcessManager(self):
        return self._processManager

    @property
    def Physics(self):
        return self._physics

    @property
    def ObjectManager(self):
        return self._objectManager

    def QuitListener(self, Event):
        """This method listens for quit events, and shuts down the 
game if there is a quit"""
        self._quit = True

    def Update(self, deltaMilliseconds):
        for event in pygame.event.get():
            if (event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE)):
                QuitEvent = Event.Event.Event(QUITTYPE, QuitData())
                self._enginePointer.EventManager.QueueEvent(QuitEvent)
                
            elif event.type == MOUSEBUTTONDOWN:
                MouseEvent = Event.Event.Event(MOUSEUPTYPE,
                                               MouseButtonEventData(
                                                   event))
                self._enginePointer.EventManager.QueueEvent(MouseEvent)
                
            elif event.type == MOUSEBUTTONUP:
                MouseEvent = Event.Event.Event(MOUSEDOWNTYPE,
                                               MouseButtonEventData(
                                                   event))
                self._enginePointer.EventManager.QueueEvent(MouseEvent)

            elif event.type == MOUSEMOTION:
                MouseEvent = Event.Event.Event(MOUSEMOTIONTYPE,
                                               MouseButtonEventData(
                                                   event))
                self._enginePointer.EventManager.QueueEvent(MouseEvent)
                
            elif event.type == KEYUP:
                KeyEvent = Event.Event.Event(KEYUPTYPE,
                                             KeyEventData(event))
                self._enginePointer.EventManager.QueueEvent(KeyEvent)
                
            elif event.type == KEYDOWN:
                KeyEvent = Event.Event.Event(KEYDOWNTYPE,
                                             KeyEventData(event))
                self._enginePointer.EventManager.QueueEvent(KeyEvent)

        #This should take care of all the rest of the subsystems
        self.ObjectManager.Update(deltaMilliseconds)
        self.ObjectManager._camera.Update(deltaMilliseconds)        
        self._enginePointer.EventManager.Update()
        self.ProcessManager.UpdateProcesses(deltaMilliseconds)

                                      

            
