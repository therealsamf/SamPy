#PGUComponent.py
from .. import Object
from .. import Renderer
from .. import Log
from .. import Event
from .. import Rect as HashRect

import pygame
from pygame.locals import *

ConvertFromPixelCoor = Renderer.Renderer.Renderer.ConvertFromPixelCoor
ConvertFromWorldCoor = Renderer.Renderer.Renderer.ConvertFromWorldCoor

AddUpdateRectData = Object.Component.AddUpdateRectData
ScheduleRenderData = Object.Component.ScheduleRenderData

#A default layer for GUI elements
GUILAYERDEFAULT = 10 

class PGUComponent(Object.Component.Component):
    name = 'PGU'
    def __init__(self, ObjectPtr):
        super().__init__(ObjectPtr)
        self._transformPtr = None
        self._rect = None
        #The actual PGU widget
        self._app = None #The 'app' that handles events and stuff
        self._eventManager = None
        self._widget = None #The actual widget that the 'app' contains
        self._screen = None

        self._ID = Object.Component.RenderComponent.ID + 1
        Object.Component.RenderComponent.ID += 1

    def Initialize(self):
        super().Initialize()
        self._transformPtr = super().GetComponent(Object.Component. \
                                                  TransformComponent)
        if self._transformPtr == None:
            Log.LogError("Failure to retrieve Transform by PGUComponent")
            return False

        gEventManager = Event.EventManager.EventManager.gEventManager
        self._eventManager = gEventManager
        if self._eventManager == None:
            Log.LogError("Retrieval of EventManager failed by PGUComponent")
            return False

        self.RegisterEventListeners()
        self.ComputeRect()
        self._screen = pygame.Surface((self._rect.w, self._rect.h))

        return True

    def Update(self, deltaMilliseconds):
        oldRect = self._rect
        self.ComputeRect()
        if oldRect != self._rect:
            """This guarantees that it's redrawn into its new position"""
            self._app.repaint()
            self.SendUpdateRectEvent(self._rect.union(oldRect))

        updateRects = self._app.update(self._screen)


        if len(updateRects) > 0:
            renderEventData = ScheduleRenderData(self._screen,
                                                 HashRect.Rectangle(
                                                     rect = pygame.Rect(0, 0,
                                                            self._rect.w,
                                                            self._rect.h)),
                                                 False,
                                                 (self._rect.x, self._rect.y),
                                                 GUILAYERDEFAULT,
                                                 self._ID,
                                                 0.0)
            self._eventManager.QueueEvent(Event.Event.Event(
                Event.GetType('ScheduleRender'),renderEventData))
            self.SendUpdateRectEvent(self._rect)

    """Sends the given rect to update, if rect == None then sends self.Rect"""
    def SendUpdateRectEvent(self, rect=None):
        r = rect
        if r == None:
            r = self._rect
        ev = Event.Event.Event(Event.GetType('AddUpdateRect'),
                               AddUpdateRectData(HashRect.Rectangle(rect = r)))
        self._eventManager.QueueEvent(ev)

    """This should be overridden in subclasses, so that we don't send keyboard
events to buttons and stuff like that"""
    def RegisterEventListeners(self):
        pass
        

    """This method computes the rect this widget occupies using the transform"""
    def ComputeRect(self):

        center = ConvertFromWorldCoor((self._transformPtr.X,
                                       self._transformPtr.Y))
        width, height = self._widget.resize()
        x, y = center[0] - width / 2, center[1] - height / 2
        self._rect = pygame.Rect(x, y, width, height)
        return self._rect
        
    def Load(self, XMLDoc):
        #Load generic PGU stuff?
        pass


