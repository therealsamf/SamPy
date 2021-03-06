from . import PGUComponent
from .. import Object
from .. import Event
from .. import Renderer

ConvertFromWorldCoor = Renderer.Renderer.Renderer.ConvertFromWorldCoor

import pgu.gui as gui
import pygame
from pygame.locals import *

class PGUTextBoxComponent(PGUComponent.PGUComponent):
    name = 'PGUTextBox'
    def __init__(self, objectPtr):
        super().__init__(objectPtr)
        self._width = 0
        self._height = 0
        
    def Initialize(self):
        if not super().Initialize():
            return False
        if self._app == None:
            self._app = gui.Desktop()
        try:
            self._app.init(widget = self._widget,
                           screen = self._screen,
                           area = pygame.Rect(0, 0, self._screen.get_width(),
                                              self._screen.get_height()))
        except BaseException as e:
            raise Object.Object.SamError(e.args[0])

        self._app.repaint(self._rect)
        return True

    def Update(self, deltaMilliseconds):
        super().Update(deltaMilliseconds)            

    def Load(self, XMLDoc):
        width = int(XMLDoc.find('width').text)
        height = int(XMLDoc.find('height').text)
        value = str(XMLDoc.find('value').text)

        self._width = width
        self._height = height
        self._widget = gui.TextArea(width = self._width,
                                    height = self._height,
                                    value = value)

    def KeyUpListener(self, EventData):
        eventDict = {'key': EventData.Key,
                     'mod': EventData.Mod}
        event = pygame.event.Event(KEYUP, eventDict)
        self._app.event(event)
    def KeyDownListener(self, EventData):
        eventDict = {'key': EventData.Key,
                     'mod': EventData.Mod,
                     'unicode': EventData.Unicode}
        event = pygame.event.Event(KEYDOWN, eventDict)
        self._app.event(event)
    def MouseButtonDownListener(self, EventData):
        coor = ConvertFromWorldCoor((EventData.X, EventData.Y))
        eventDict = {'pos': (coor[0] - self._rect.x, coor[1] - self._rect.y),
                     'button': EventData.Button}
        event = pygame.event.Event(MOUSEBUTTONDOWN, eventDict)
        self._app.event(event)
    def MouseButtonUpListener(self, EventData):
        coor = ConvertFromWorldCoor((EventData.X, EventData.Y))
        eventDict = {'pos': (coor[0] - self._rect.x, coor[1] - self._rect.y),
                     'button': EventData.Button}
        event = pygame.event.Event(MOUSEBUTTONUP, eventDict)
        self._app.event(event)
    def MouseMotionListener(self, EventData):
        eventDict = {'pos': (EventData.X, EventData.Y),
                     'rel': EventData.Rel,
                     'buttons': EventData.Buttons}
        event = pygame.event.Event(MOUSEMOTION, eventDict)
        self._app.event(event)
        
    def RegisterEventListeners(self):
        try:
            self._eventManager.RegisterDelegate(Event.GetType('MouseMove'),
                                                self.MouseMotionListener)
            self._eventManager.RegisterDelegate(Event.GetType('MouseButtonUp'),
                                                self.MouseButtonUpListener)
            self._eventManager.RegisterDelegate(Event.GetType('MouseButtonDown'),
                                                self.MouseButtonDownListener)
            self._eventManager.RegisterDelegate(Event.GetType('KeyDown'),
                                                self.KeyDownListener)
            self._eventManager.RegisterDelegate(Event.GetType('KeyUp'),
                                                self.KeyUpListener)
        except BaseException as e:
            raise Object.Object.SamError('Failure to RegisterEventListeners')
            
