#AnimationComponent.py

from . import Component
from .. import Log
from .. import Rect
from .. import Event

hashRect = Rect.Rectangle

import pygame
from pygame.locals import *

class AnimationComponent(Component.Component):
    name = 'Animation'
    def __init__(self, Object):
        super().__init__(Object)
        self._renderComponent = None
        self._animations = dict()
        self._lastUpdate = 0
        self._currentAnim = None
        self._lastRect = None
        

    def Update(self, deltaMilliseconds):
        if (self._currentAnim != None):
            if (self._lastUpdate + deltaMilliseconds > self._currentAnim.CurrentSpeed * 1000):
                newRect = self._currentAnim.nextRect()
                self._renderComponent.SetRect(rect =
                                              newRect)
                if newRect != self._lastRect:
                    self._renderComponent.SendUpdateRectEvent()
                self._lastRect = newRect
                self._lastUpdate = 0
            else:
                self._lastUpdate += deltaMilliseconds

    def Initialize(self):
        #This is actually used in this component to grab the renderer component
        #on this object
        self._renderComponent = super().GetComponent(Component.RenderComponent)
        if (self._renderComponent == None):
            return False

        if self._currentAnim != None:
            self.ChangeAnimation(self._currentAnim.Name, True)



        return True

    def ChangeAnimation(self, animName, override=False):
        animName = animName.lower()
        if self._currentAnim and self._currentAnim.Name == animName and \
           not override:
            return
        Log.LogMessage("Animation wants to change to: " + str(animName))
        if self._currentAnim:
            self._currentAnim.reset()
        if (animName in self._animations):
            self._currentAnim = self._animations[animName]
            Log.LogMessage("Change of animation was successfull")
            if (self._currentAnim.Surface != \
                self._renderComponent.SurfaceName or \
                (type(self._currentAnim.Surface) != str and \
                 self._currentAnim.Name != self._renderComponent.SurfaceName)):
                self._renderComponent.ChangeSurface(
                    self._currentAnim.Surface,
                    self._currentAnim.nextRect(), self._currentAnim.Name)

                

            

    def Load(self, XMLElement):
        """For every animation sequence, we have a name, a list of ordered 
rects, and a surface string, and a default speed for the animation"""
        for child in XMLElement:
            if child.tag.find('anim') != -1:
                anim = Animation()
                if not anim.Load(child):
                    Log.LogError("Failure to load animation !")
                    return False
                self._animations[anim.Name] = anim
        #This is mainly just convenience for debug, normally there
        #would be a Animation controller that would do this
        try:
            currentAnim = XMLElement.find('current').text
            self._currentAnim = Animation()
            self._currentAnim.Name = currentAnim            
        except BaseException:
            return True
        
        return True

    def AddAnimation(self, name, rects, speed, surface):
        self._animations[name] = Animation(name, rects, speed, surface)

    def GetSurface(self):
        if self._currentAnim != None:
            if type(self._currentAnim.Surface) != str:
                return self._currentAnim.Surface
            else:
                #Get surface from resource cache, or rendercomponent
                #return said surface
                pass

    """This method is for elements that don't load their surfaces, 
they create them"""
    def AddSurface(self, surface):
        self._renderComponent.ChangeSurface(surface, None, 'default')
        self._animations['default'] = Animation('default', None, 0, 'default')
        


class Animation():
    """This is for everything needed with one animation:
a list of rects, a surface name, a default speed, and a name"""
    def __init__(self, name=None, rects=list(), speed=0, surface=None):
        self._name = name
        if self._name != None:
            self._name = self._name.lower()
        self._rects = rects
        self._speed = speed
        self._currentSpeed = self._speed
        self._surface = surface

        #These are used by the AnimationComponent
        self._currentRectIndex = 0

    def Load(self, XMLElement):
        """This method takes a child of an animation component to load to an
actual animation"""

        #Get the rects
        rects = XMLElement.find("rects")
        for element in rects.findall('rect'):
            r = hashRect()
            r.Load(element)
            self._rects.append(r.Rect)

        self.ResetRect()
        #Get the speed
        self._speed = float(XMLElement.find('speed').text)
        self._currentSpeed = self._speed
        #Get the name
        self._name = XMLElement.find('name').text.lower()
        Log.LogMessage("Name of this animation = " + self._name)
        self._surface = XMLElement.find('surface').text

        return True

    def ResetRect(self):
        self._currentRectIndex = 0

    def nextRect(self):
        self._currentRectIndex += 1
        if (self._currentRectIndex == len(self._rects)):
            self._currentRectIndex = 0
        return self._rects[self._currentRectIndex]

    def ResetSpeed(self):
        self.CurrentSpeed = self.Speed

    def reset(self):
        self.ResetSpeed()
        self.ResetRect()
        
    @property
    def Name(self):
        return self._name
    #Once set, self._name should never be reset
    #... unless the at the very beginning...

    @Name.setter
    def Name(self, value):
        self._name = value
    
    @property
    def Speed(self):
        return self._speed
    #Once set, self._speed should never be reset

    @property
    def CurrentSpeed(self):
        return self._currentSpeed

    @CurrentSpeed.setter
    def CurrentSpeed(self, value):
        self._currentSpeed = value

    @property
    def Rects(self):
        return self._rects
    #Rects doesn't get a setter, shouldn't be really set outside of this classes
    #initialization, which will happen in this own class

    @property
    def Surface(self):
    #This is not a pygame.Surface object, it's just the name of a surface
        return self._surface
    #Surface should never be changed once set either



class ChangeAnimationEventData(Event.Event.EventData):
    """This class is mainly just for debug. There would be too many of these
things if this was actually used"""
    def __init__(self, animName):
        super().__init__()
        self._animName = animName

    @property
    def AnimName(self):
        return self._animName
