#GuiComponent.py

from . import Object
from . import Component
from . import AnimationComponent
from .. import Log
from .. import Renderer
from .. import Engine

import pygame

ConvertFromWorldCoor = Renderer.Renderer.Renderer.ConvertFromWorldCoor

class GuiComponent(Component.Component):
    name = 'Gui'
    def __init__(self, Object):
        super().__init__(Object)
        self._renderComponent = None
        self._animationComponent = None
        self._transformComponent = None
        self._width = 0
        self._height = 0
        self._hitbox = None
        self._theme = None

        self._visible = False
        self._greyedout = False
        self._capturing = False

    @property
    def Hitbox(self):
        return self._hitbox

    def Initialize(self):
        """This method is where we need to call the get the theme and render
this gui component"""
        #Pseudocode
        #Grab theme
        #see what surfaces we need from the theme
        #get surfaces from resource cache
        #pass all these surfaces to our render method

        self._renderComponent = super().GetComponent(
            Component.RenderComponent)
        self._animationComponent = super().GetComponent(
            AnimationComponent.AnimationComponent)
        self._transformComponent = super().GetComponent(
            Component.TransformComponent)
        self.SetHitbox()
        if not issubclass(self._theme.__class__,
                          Component.Component):

            if self._theme.find('.css') == -1:
                self._theme = self._theme + '.css'

            self._theme = Engine.Engine.gEngine.GameLogic. \
                          ObjectManager.GetObjectsFromName(
                              self._theme).pop()
            self._theme = self._theme.GetComponent('theme')

        

        return self._transformComponent != None and \
                self._renderComponent != None and \
                    self._animationComponent != None
                                                                    


    def Render(self, *args, **kwargs):
        """This method will be overridden for every widget"""
        pass

    def Update(self, deltaMilliseconds):
        """This method was inherited from Component. For gui, I don't think
we'll need an update function, just listeners from event"""
        pass

    def Load(self, XMLDoc):
        """This method we'll load ourselves from an XML doc in a .tmx file"""
        self._theme = XMLDoc.find('theme').text
        if self._theme == None:
            Log.LogMessage("Theme retrieval isn't working!")

    def SetHitbox(self):
        """This method takes our tranform, width, and height and creates the 
hitbox that we need"""
        #We're going to use a pygame.Rect for the hitbox

        #Width and height should be set from self.Load()
        
        x = self._transformComponent.X - (self._width / 2)
        y = self._transformComponent.Y - (self._height / 2)
        coordinates = ConvertFromWorldCoor((x, y))
        self._hitbox = pygame.Rect(coordinates[0], coordinates[1], self._width, self._height)

    def Collide(self, coor):
        """This method tests itself against the hitbox of this widget.
It only accepts one tuple, because I'm assuming that this argument is being
passed from pygame.mouse.get_pos()"""
        cX = coor[0]
        cY = coor[1]
        if not (self._hitbox.x <= cX <= self._hitbox.x + self._hitbox.width):
            return False
        if not (self._hitbox.y <= cY <= self._hitbox.y + self._hitbox.height):
            return False

        return True

    def DisplayTooltip(self):
        """The tooltip will have to be its own object, with just a tooltip
component. It will have to render itself as well according to a theme, and have
set width and height. I'll put a pointer to the tooltip object for this object
on this object during the self.Load() method"""

        #We need to figure out where this widget is in the screen, and
        #from what corner we need to display the tool tip
        #Then we call the display method on the tool tip, setting the right
        #corner to display from
        #self._tooltip.display
        pass

    @property
    def Visible(self):
        return self._visible

    @Visible.setter
    def Visible(self, boolean):
        if type(boolean) == bool:
            self._visible = boolean

    def OnHover(self, coor):
        """This method is to be overridden by child widgets"""
        #One thing this method should do is change the animation to a
        #'hover' animation if the
        #animation component has it
        if not self._greyedout:
            self._animationComponent.ChangeAnimation('hover')


    def OnClick(self, coor):
        """This method is to be overridden by child widgets"""
        #One thing this method should do is change the animation to a 'click'
        #animation, if the
        #animation component has it
        if not self._greyedout:
            self._animationComponent.ChangeAnimation('active')

    def OnClickUp(self, coor):
        """This method is to be overridden by child widgets"""
        #Note: This should only be called if this widget is clicked and on this
        #widget, and the button is
        #released while on this widget
        #This should change the animation back to the default before calling
        #something that
        #will be written in the child implementations
        if not self._greyedout:
            self._animationComponent.ChangeAnimation('default')
        if self._capturing:
            self.Release()

    def GreyOut(self):
        """This sets the GUI object to a 'greyedout' state. It won't receive events and should change the 
animation. This should usually be overridden"""
        self._animationComponent.ChangeAnimation('grey')
        self._greyedout = True

    def Restore(self):
        """This method undoes the 'greyingout'"""
        self._animationComponent.ChangeAnimation('Default')
        self._greyedout = False

    def GetAbsCoor(self, coor):
        """This method is for child gui objects of contianers, 
to see where there absolute position on the screen is"""
        #This returns the center of the object, i.e. the transform
        return (self._transformComponent.X + coor[0],
                self._transformComponent.Y + coor[1])

    def CaptureEvents(self):
        """This method is to make sure that if you've clicked a button,
 then while holding the mouse down you move the cursor all over the screen,
 all the events are being sent to that button, not everything else"""
        #We'll see if this works...
        EventManager = Engine.Engine.gEngine.EventManager
        EventManager.Capture(self)
        self._capturing = True

    def Release(self):
        """This method undoes the method described above"""
        if self._capturing:
            EventManager = Engine.Engine.gEngine.EventManager
            EventManager.Release()
            self._capturing = False
        

        
        
class GuiContainer(GuiComponent):
    name = GuiComponent.name + "Container"
    """This class has a field to contain other gui objects"""
    def __init__(self, Object):
        super().__init__(Object)
        self._widgets = None

    def Initialize(self):
        """This method will initialize our container after all the resources have been loaded into the
resource cache and all the child objects have been called their 'Load' method"""
        super().Initialize()


    def Render(self):
        """This method will render only this container"""
        pass

    def Load(self, XMLElement):
        """This method will load this component according to the XML Doc"""
        #This method also needs to construct its self._widgets
        self._widgets = list()

    def OnClick(self, coor):
        """This coor should be in pixel coordinates,
 we should error if it's not"""
        if Engine.DebugMode == True:
            if type(coor[0]) != int:
                Log.LogError("Attempting to pass an " + \
                             "invalid coordinate parameter to " + \
                             "'OnClick' for a container!")
                return
        else:
            for widget in self._widgets:
                nCoor = (coor[0] + \
                         ConvertFromWorldCoor(self._transformComponent.X),
                         coor[1] + \
                         ConvertFromWorldCoor(self._transformComponent.Y))
                if widget.Collide(nCoor):
                    stop = widget.OnClick(nCoor)
                    if stop:
                        break
    def OnClickUp(self, coor):
        """This coor should be in pixel coordinates, 
we should error if it's not"""
        if Engine.DebugMode == True:
            if type(coor[0]) != int:
                Log.LogError("Attempting to pass an invalid " + \
                             "coordinate parameter to 'OnClick' " + \
                             "for a container!")
                return
        else:
            for widget in self._widgets:
                nCoor = (coor[0] + \
                         ConvertFromWorldCoor(self._transformComponent.X),
                         coor[1] + \
                         ConvertFromWorldCoor(self._transformComponent.Y))
                if widget.Collide(nCoor):
                    stop = widget.OnClick(nCoor)
                    if stop:
                        break
    
    def OnHover(self, coor):
        """This coor should be in pixel coordinates, 
we should error if it's not"""
        if Engine.DebugMode == True:
            if type(coor[0]) != int:
                Log.LogError("Attempting to pass an invalid " + \
                             "coordinate parameter to 'OnClick'" + \
                             " for a container!")
                return
        else:
            for widget in self._widgets:
                nCoor = (coor[0] + \
                         ConvertFromWorldCoor(self._transformComponent.X),
                         coor[1] + \
                         ConvertFromWorldCoor(self._transformComponent.Y))
                if widget.Collide(nCoor):
                    stop = widget.OnHover(nCoor)
                    if stop:
                        break



class LabelGuiComponent(GuiComponent):
    name = "gui.label"
    def __init__(self, Object):
        super().__init__(Object)
        self._text = None
        #text size
        self._size = 0


    def Load(self, XMLElement):
        super().Load(XMLElement)
        self._text = XMLElement.find('text').text
        
        
    def Initialize(self):
        super().Initialize()
        surface = self.Render()
        self._animationComponent.AddAnimation('default', [
            surface.get_rect()], 1, surface)
        self._animationComponent.ChangeAnimation('default')

        self.SetHitbox()
        return True


    def Render(self):
        surface, width, height = RenderLabel(self._theme, 'label', self._text)
        self._width = width
        self._height = height
        return surface

def RenderLabel(theme, selector, text):
    #We use a 16px scale
    size = theme.GetProperty(selector, 'font-size')
    size = GetPixel(size[0])
    color = theme.GetProperty(selector, 'color')[0]
    if color != None and color.type == "HASH":
        color = ConvertFromHex(color)
    backgroundColor = theme.GetProperty(selector,
                                            'background-color')[0]
    if backgroundColor != None and backgroundColor.type == "HASH":
        backgroundColor = ConvertFromHex(backgroundColor)

    font = theme.GetProperty(selector, 'font-family')
    realFont = None
    ResourceCache = Engine.Engine.gEngine.ResourceCache
    for token in font:
        realFont = ResourceCache.GetResource(token.value)
        if realFont != None:
            break

    font = realFont

    padding = theme.GetProperty(selector, 'padding')
    paddingList = list()
    for token in padding:
        if token.type == "DIMENSION" or token.type == 'PERCENTAGE':
            pixelSize = GetPixel(token)
            paddingList.append(pixelSize)

    padding = paddingList
    width = theme.GetProperty(selector, 'width')
    width = GetPixel(width[0])
    height = theme.GetProperty(selector, 'height')
    height = GetPixel(height[0])

    margin = theme.GetProperty(selector, 'margin')
    marginList = list()
    for token in margin:
        if token.type == 'DIMENSION' or token.type == 'PERCENTAGE':
            pixelSize = GetPixel(token)
            marginList.append(pixelSize)

    margin = marginList

    borderColor = theme.GetProperty(selector, 'border-color')[0]
    if borderColor != None and borderColor.type == 'HASH':
        borderColor = ConvertFromHex(borderColor)

    borderWidth = theme.GetProperty(selector, 'border-width')
    borderWidthList = list()
    for token in borderWidth:
        if token.type == 'DIMENSION' or token.type == 'PERCENTAGE':
            pixelSize = GetPixel(token)
            borderWidthList.append(pixelSize)

    borderWidth = borderWidthList

    fontSurface = font.Render(text, size, True, color,
                              backgroundColor)
    if fontSurface.get_width() + padding[1] + padding[3] > width:
        width = fontSurface.get_width() + padding[1] + padding[3]
    if fontSurface.get_height() + padding[0] + padding[2] > height:
        height = fontSurface.get_height() + padding[0] + padding[2]


    Surface = pygame.Surface((margin[3] + width + \
                              margin[1],
                              margin[0] + height + \
                              margin[2]))
    fontRect = fontSurface.get_rect(center=(margin[3] + width / 2,
                                            margin[0] + height / 2))
    if backgroundColor != None:
        Surface.fill(backgroundColor)
    Surface.blit(fontSurface, fontRect)
    if borderColor != None:
        pygame.draw.rect(Surface, borderColor, pygame.Rect(
            margin[3], margin[0] - borderWidth[0] / 2,
            width, borderWidth[0]))
        pygame.draw.rect(Surface, borderColor, pygame.Rect(
            margin[3] - borderWidth[3] / 2,
            margin[0], borderWidth[3], height))
        pygame.draw.rect(Surface, borderColor, pygame.Rect(
            Surface.get_width() - margin[1] - borderWidth[1] / 2,
            margin[0],
            borderWidth[1], height))
        pygame.draw.rect(Surface, borderColor, pygame.Rect(
            margin[3],
            Surface.get_height() - margin[2] - borderWidth[2] / 2,
            width, borderWidth[2]))

    return Surface, width, height

def ConvertFromHex(Number):
    number = Number.value
    r = int(number[1:3], 16)
    g = int(number[3:5], 16)
    b = int(number[5:7], 16)
    return (r, g, b)

def GetPixel(token, default = 16):
    if token.type == "DIMENSION":
        if token.unit == 'px':
            return token.value
        elif token.unity == 'em':
            return token.value * default
    elif token.type == 'PERCENTAGE' and token.unit == '%':
        return (token.value / 100.0) * default

    return 0
                
        
        
    

    


    

        
        

