#QuadTree.py

from .. import Log
from .. import Renderer
from . import Event

import pygame

class QuadTree():
    """This class is used to store gui objects in an efficient way for mouse collision
testing. It might also be used for all objects that just don't need physics"""
    MAXELEMENTS = 4
    START = (0, 0)
    END = (Renderer.Renderer.SCREEN_DIMENSIONS[0], Renderer.Renderer.SCREEN_DIMENSIONS[1])
    def __init__(self):
        self._partition = None
        self._lastComponent = None

    def Initialize(self, eventManager):
        self._partition = Partition(QuadTree.START[0],
                                     QuadTree.START[1],
                                     QuadTree.END[0],
                                     QuadTree.END[1])

        eventManager.RegisterDelegate('ObjectCreated',
                                      self.AddElementListener)

        return True

    def CollideElement(self, coor):
        """This method takes a given coor and finds an element that the coor might
have collided with. If it finds one, it returns the pointer to the element"""
        #Check to see if it was the last element returned
        if self._lastComponent != None and self._lastComponent.Collide(coor):
            return self._lastComponent.Object
        
        nPart = self._partition.GetPartition(coor)
        for element in nPart.Elements:
            Gui = GetGui()
            guiComponent = element.GetComponent(Gui)
            if guiComponent.Collide(coor):
                self._lastComponent = guiComponent
                return element
        self._lastComponent = None
        return None

    def AddElement(self, element):
        """This method takes a given element and adds it to the quadtree.
 The quadtree rearranges itself if the element unbalances it"""
        self._partition.AddElement(element)

    def AddElementListener(self, objekt):
        Log.LogMessage("Called QuadTree event delegate")
        self._partition.AddElement(objekt.Object)

class Partition():
    """This class is a helper struct to QuadTree by storing the rect size of the partition. It also stores the gui objects inside this partition"""
    def __init__(self, x, y, width, height):
        self._elements = set()
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._subPartitions = None

    @property
    def Elements(self):
        return self._elements

    def AddElement(self, element):        
        guiComp = element.GetComponent(GetGui())
        if guiComp != None:
            Log.LogMessage("Added Gui Component")
            if self._subPartitions == None:
                self._elements.add(element)
                if len(self._elements) > QuadTree.MAXELEMENTS:
                    self.Subdivide()
            else:
                for partition in self._subPartitions:
                    if partition.Collide(guiComp):
                        partition.AddElement(element)
                

    def GetPartition(self, coor):
        if self._subPartitions == None:
            return self
        else:
            selection = list()
            x = coor[0]
            y = coor[1]
            if (x < self.Width / 2):
                selection.append(0)
                selection.append(2)
            else:
                selection.append(1)
                selection.append(3)
            if (y < self.Height / 2):
                return self._subPartitions[selection[0]].GetPartition(coor)
            else:
                return self._subPartitions[selection[1]].GetPartition(coor)

    def Subdivide(self):
        """This method is called when the number of elements in this partition has
exceeded the QuadTree.MAXELEMENTS. It subdivides itself into 4 partitions and places the
stored elements into each partition accordingly"""
        self._subPartitions = list()
        self._subPartitions[0] = Partition(self.X, self.Y, self.Width / 2, self.Height / 2)
        self._subPartitions[1] = Partition(self.X + (self.Width / 2),
                                        self.Y, self.Width / 2, self.Height / 2)
        self._subPartitions[2] = Partition(self.X, self.Y + (self.Height / 2),
                                           self.Width / 2, self.Height / 2)
        self._subPartitions[3] = Partition(self.X + (self.Width / 2),
                                           self.Y + (self.Height / 2),
                                           self.Width / 2,
                                           self.Height / 2)
        for element in self._elements:
            GuiComponent = element.GetComponent(GetGui())
            for partition in self._subPartitions:
                if partitiion.Collide(GuiComponent):
                    partition.AddElement(element)
                

    def Collide(self, GuiComponent):
        """This method takes a GuiObject and figures if it collides within this Partition"""
        hitbox = GuiComponent.Hitbox
        rect = pygame.Rect(self.X, self.Y, self.Width, self.Height)
        if rect.colliderect(hitbox):
            return True
        return False

    @property
    def X(self):
        return self._x

    @property
    def Y(self):
        return self._y

    @property
    def Width(self):
        return self._width

    @property
    def Height(self):
        return self._height


def GetGui():
    from .. import Object
    return Object.GuiComponent.GuiComponent
    

    

    
    
