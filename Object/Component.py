#Component.py

from .. import Log
from .. import Renderer
from .. import Resource
from .. import Rect
from .. import Event

hashRect = Rect.Rectangle
import pygame, math
from pygame.locals import *

ConvertFromWorldCoor = Renderer.Renderer.Renderer.ConvertFromWorldCoor
ConvertFromPixelCoor = Renderer.Renderer.Renderer.ConvertFromPixelCoor

class Component():
    name = 'Base'
    def __init__(self, Object):
        self._objectPtr = Object

    def Initialize(self):
        return True

    def Update(self, deltaMilliseconds):
        pass


    def Load(self, XMLDoc):
        #method to load the component from an XML representation
        Log.LogMessage("Attempting to Load Component: " + self.name)

    def Require(self, ComponentType):
        if (not self._objectPtr.CheckComponent(ComponentType.name)):
            raise AttributeError("Component: " + ComponentType.name + " not found in the parent object!")
        

    def GetComponent(self, ComponentType):
        """This method returns a reference to another component on the same game object
this shouldn't be called every frame, it should be called at startup"""
        if (ComponentType == self.__class__): #This technically shouldn't happen...
            Log.LogWarning("Component attempting to grab itself!")
            return self
        else:
            try:
                self.Require(ComponentType)
                return self._objectPtr.GetComponent(ComponentType.name)
            except AttributeError:
                Log.LogError("Attempting to get a component that doesn't exist on this object!")
                return None

    @property
    def Object(self):
        return self._objectPtr



#Now to define common components

class TransformComponent(Component):
    """Transform component for every object in the game. MUST BE IN WORLD 
COORDINATES! This also keeps track of the center of the object, not topleft"""

    #This component should be directly modified by other components
    #This component won't have an update function that updates itself
    name = "transform"
    def __init__(self, Object):
        super().__init__(Object)
        self._x = 0
        self._y = 0
        self._z = 0
        self._rotation = 0
        self._scale = 1

    def Load(self, XMLElement):
        """This is for initialization from an XML element. Doesn't necessarily
have to be fast"""
        super().Load(XMLElement)
        self._x = float(XMLElement.find('x').text)
        self._y = float(XMLElement.find('y').text)
        self._z = float(XMLElement.find('z').text)
        self._rotation = float(XMLElement.find('rotation').text)
        self._scale = float(XMLElement.find('scale').text)

    #Accessors to all fields
    @property
    def X(self):
        return self._x

    @X.setter
    def X(self, value):
        #Maybe error check to detect bad values?
        self._x = value

    @property
    def Y(self):
        return self._y

    @Y.setter
    def Y(self, value):
        self._y = value

    @property
    def Z(self):
        return self._z

    @Z.setter
    def Z(self, value):
        self._z = value

    @property
    def Rotation(self):
        return self._rotation

    @Rotation.setter
    def Rotation(self, value):
        self._rotation = value

    @property
    def Scale(self):
        return self._scale

    @Scale.setter
    def Scale(self, value):
        self._scale = value

    
class RenderComponent(Component):
    """This component is for keeping track of the surface or rect of a 
surface to render. It also keeps track of the layer that it is to be drawn"""
    name = 'Render'
    ID = 0
    def __init__(self, Object):
        super().__init__(Object)
        self._surface = None
        self._rect = None
        self._layer = 0
        self._surfaceName = None
        self._worldRect = None #This is the rect of this object in the world!
        self._transform = None
        self._flip = None
        self._id = RenderComponent.ID + 1
        self._quadPartition = None
        RenderComponent.ID += 1

        self._lastCoor = (0, 0)

    @property
    def QuadPartition(self):
        return self._quadPartition
    @QuadPartition.setter
    def QuadPartition(self,value):
        self._quadPartition = value
    

    def Load(self, XMLElement):
        """This loads the component from the given XML element"""

        super().Load(XMLElement)
        self._surfaceName = str(XMLElement.find('surface').text)
        if self._surfaceName.lower() in ['', 'none']:
            self._surface == None
        else:
            self._surface = Resource.ResourceCache.ResourceCache.gResourceCache.GetResource(self._surfaceName);
        
        self._layer = int(XMLElement.find('layer').text)
        #Create a new hashable rect        
        sRect = hashRect()
        #Load the rect from an xml child node
        sRect.Load(XMLElement.find('rect'))
        if sRect.Rect.width == 0 and self._surface != None:
            sRect.Rect.width = self._surface.get_width()
        if sRect.Rect.height == 0 and self._surface != None:
            sRect.Rect.height = self._surface.get_height()
        
        self._rect = sRect
        Log.LogMessage("Initial Rect = " + str(self._rect))
            
        self._flip = XMLElement.find('flip').text in ['True', 'true', 't', 'T']

        self._transform = super().GetComponent(TransformComponent)
        transformPointer  = self._transform
        if transformPointer != None:
            pixelCoor = ConvertFromWorldCoor((transformPointer.X, transformPointer.Y))
            halfWidth = self._rect.w / 2
            halfHeight = self._rect.h / 2
            self._worldRect = hashRect(x = pixelCoor[0] - halfWidth,
                                       y = pixelCoor[1] - halfHeight,
                                       w = self._rect.w, h = self._rect.h)
        else:
            self._worldRect = None

    def Initialize(self):
        if (self._transform == None):
            self._transform = super().GetComponent(TransformComponent)
            #Now if we still don't have the transform, then we have a problem
            if (self._transform == None):
                return False
        if (self._worldRect == None):            
            self.SetWorldRect(True)


        if self._worldRect.w != 0 and self._worldRect.h != 0:
            eData = AddUpdateRectData(self._worldRect)
            eType = Event.GetType('AddUpdateRect')
            Event.EventManager.EventManager.gEventManager.QueueEvent(
                Event.Event.Event(eType, eData))

        return True

    def Update(self, deltaMilliseconds):        
        #Update the world rect, according to the transform
        oldRect = self._worldRect
        """        pixelCoor = ConvertFromWorldCoor((self._transform.X,
                                          self._transform.Y))
        halfWidth = self._rect.w / 2
        halfHeight = self._rect.h / 2
        self._worldRect = hashRect(x = pixelCoor[0] - halfWidth,
                               y = pixelCoor[1] - halfHeight,
                               w = self._rect.w,
                               h = self._rect.h)
"""
        self.SetWorldRect()
        if oldRect != self._worldRect:
            eData = AddUpdateRectData(oldRect)
            eType = Event.GetType('AddUpdateRect')
            Event.EventManager.EventManager.gEventManager.QueueEvent(
                Event.Event.Event(eType, eData))
            eData = AddUpdateRectData(self._worldRect)
            Event.EventManager.EventManager.gEventManager.QueueEvent(
                Event.Event.Event(eType, eData))

    def SendUpdateRectEvent(self, rect = None):
        """This method is primarily used by the animation component. The
Animation component changes the image of this render and needs the renderer
to know that this world rect needs updating"""
        if rect == None:
            rect = self._worldRect
        eData = AddUpdateRectData(rect)
        eType = Event.GetType('AddUpdateRect')
        Event.EventManager.EventManager.gEventManager.QueueEvent(
            Event.Event.Event(eType, eData))

                        

    def Schedule(self, offset = None):
        if (offset != None):
            coor = (self._worldRect.Rect.topleft[0] - offset[0],
                    self._worldRect.Rect.topleft[1] - offset[1])
        else:
            coor = self._worldRect.Rect.topleft
        

        eData = ScheduleRenderData(self._surface, self._rect,
                                   self._flip, coor, self._layer, self._id,
                                   self._transform.Rotation)
        eType = Event.GetType('ScheduleRender')
        Event.EventManager.EventManager.gEventManager.QueueEvent(
            Event.Event.Event(eType, eData))

    def CollideRect(self, rect):
        return self._worldRect.colliderect(rect)
        
    #Accessors
    @property
    def Surface(self):
        return self._surface

    @Surface.setter
    def Surface(self, value):
        #This shouldn't be called often, the rect field should usually be the
        #thing that is changing
        if not isinstance(value, pygame.Surface):
            return
        self._surface = value


    def ChangeSurface(self, surfaceName, newRect, othername = None):
        #Load this surface from the resource cache
        if isinstance(surfaceName, pygame.Surface):
            self.Surface = surfaceName
            if othername:
                self._surfaceName = othername
        else:
            surface = Resource.ResourceCache.ResourceCache.gResourceCache.GetResource(surfaceName)
            self.Surface = surface
            self._surfaceName = surfaceName
        self.SetRect(rect = newRect, forceUpdate = True)
        """This is an attempt to fix a bug before it gets here. If the following
line is unnecessary then remove it"""
        self.SendUpdateRectEvent()
        
    @property
    def Rect(self):
        #This is the rect on the surface to tell what's the current surface
        #This has NOTHING to do with the objects game-world position
        return self._rect

    @property
    def SurfaceName(self):
        return self._surfaceName

    @property
    def Flip(self):
        return self._flip

    @Flip.setter
    def Flip(self, value):
        self._flip = value                    
    
    def SetRect(self, **kwargs):
        oldRect = self._rect
        if (len(kwargs) == 0):
            #The whole surface is to be the rect
            if (self._surface != None):
                self._rect = self._surface.get_rect()
                self._rect = hashRect(x = self._rect.x,
                                      y = self._rect.y,
                                      w = self._rect.w,
                                      h = self._rect.h)
        else:
            x = kwargs.get('x', 0)
            y = kwargs.get('y', 0)
            w = kwargs.get('w', 0)
            h = kwargs.get('h', 0)
            rect = kwargs.get('rect', None)
            if (rect == None):
                self._rect = hashRect(x = x, y = y, w = w, h = h)

            else:
                if isinstance(rect, pygame.Rect):
                    self._rect = hashRect(x = rect.x,
                                          y = rect.y,
                                          w = rect.w,
                                          h = rect.h)

        forceUpdate = False or kwargs.get('forceUpdate', False)
        if oldRect.w != self._rect.w or \
           oldRect.h != self._rect.h:
            forceUpdate = True
            """This is needed because otherwise animations that change
            the dimensions of the surface won't have an UpdateRect in
            the Renderer"""
            self.SendUpdateRectEvent()

        self.SetWorldRect(forceUpdate)

    def SetWorldRect(self, forceUpdate=False):
        """This method updates the world rect that the renderer will blit the
image to on screen. To be efficient this method only updates the world rect
if needed. Also, when the world rect is moved then the render component's
quad partition will be pinged to update itself, incase we've left the quad 
partition's boundaries"""
        pixelCoor = ConvertFromWorldCoor((self._transform.X, self._transform.Y))
        
        halfWidth = self._rect.w / 2
        halfHeight = self._rect.h / 2
        updateRect = True
        if halfWidth != 0 and halfHeight != 0 and self._lastCoor != pixelCoor:
            self._lastCoor = pixelCoor
        else:
            updateRect = False
        if updateRect or forceUpdate:
            Log.LogMessage("Calculating WorldRect")
            wRect = hashRect(x = pixelCoor[0] - halfWidth,
                             y = pixelCoor[1] - halfHeight,
                             w = self._rect.w, h = self._rect.h)
            if self._transform != None and self._transform.Rotation != 0:
                corners = self.RotateRect(wRect.Rect, self._transform.Rotation)
                minX = min(corners[0][0], min(
                    corners[1][0], min(
                        corners[2][0], corners[3][0])))
                maxX = max(corners[0][0], max(
                    corners[1][0], max(
                        corners[2][0], corners[3][0])))
                minY = min(corners[0][1], min(
                    corners[1][1], min(
                        corners[2][1], corners[3][1])))
                maxY = max(corners[0][1], max(
                    corners[1][1], max(
                        corners[2][1], corners[3][1])))
                wRect = hashRect(x = minX,
                                 y = minY,
                                 w = maxX - minX,
                                 h = maxY - minY)
                Log.LogMessage("Rect right after rotation: " + \
                               str(wRect.Rect))
            
            self._worldRect = wRect

            if self.QuadPartition != None:
                self.QuadPartition.UpdatePartition()

    def RotateRect(self, rect, rotation):
        origin = self._transform
        originX = 0
        originY = 0

        if origin != None:
            (originX, originY) = ConvertFromWorldCoor((origin.X, origin.Y))
        corners = list()
        for corner in [rect.topleft, rect.topright,
                       rect.bottomright, rect.bottomleft]:
            tempX = corner[0] - originX
            tempY = corner[1] - originY
            rotateX = tempX * math.cos(math.radians(rotation)) - \
                      tempY * math.sin(math.radians(rotation))
            rotateY = tempX * math.sin(math.radians(rotation)) + \
                      tempY * math.cos(math.radians(rotation))
            corner = (rotateX + originX, rotateY + originY)
            corners.append(corner)

        return corners
        

    @property
    def WorldRect(self):
        return self._worldRect

    @property
    def Layer(self):
        return self._layer

    @Layer.setter
    def Layer(self, value):
        self._layer = value

                

class ScheduleRenderData(Event.EventData):
    """This class is data for the ScheduleRender event. The constructor 
takes a rect, an image, a flip boolean, a layer int, and a coordinate tuple"""
    def __init__(self, surface, area, flip, coor, layer, ID,
                 rotation):
        super().__init__()
        self._surface = surface
        self._area = area
        self._flip = flip
        self._coor = coor
        self._layer = layer
        self._ID = ID
        self._rotation = rotation

    @property
    def Rotation(self):
        return self._rotation
    @property
    def ID(self):
        return self._ID

    @property
    def Layer(self):
        return self._layer
    @property
    def Flip(self):
        return self._flip
    @property
    def Coor(self):
        return self._coor
    @property
    def Area(self):
        return self._area
    @property
    def Surface(self):
        return self._surface
        
class AddUpdateRectData(Event.EventData):
    """This class is data for the AddUpdateRect event. The constructor
takes a hashRect object, rather than a pygame.rect"""
    def __init__(self, rect):
        super().__init__()
        self._rect = rect
        
    @property
    def Rect(self):
        return self._rect
        
    
    
    

    
