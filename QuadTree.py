#QuadTree.py

from . import Log

import pygame

class QuadTree():
    """This class is used to store gui objects in an efficient way for mouse collision
testing. It might also be used for all objects that just don't need physics"""
    MAXELEMENTS = 4
    def __init__(self, startCoor, endCoor):
        self._partition = None
        self._lastComponent = None
        self._start = startCoor
        self._end = endCoor

    def Initialize(self):
        self._partition = Partition(self._start[0],
                                     self._start[1],
                                     self._end[0],
                                     self._end[1])
        return True

    def CollideElement(self, rect):
        """This method takes a given rect and finds an element that the coor
 might have collided with. If it finds one, it returns the pointer to the
 element"""

        partList = list()
        self._partition.CollideRect(rect, partList)
        objects = set() #so that we don't return duplicates
        for partition in partList:
            for objekt in partition.Elements:
                if rect.colliderect(objekt.WorldRect.Rect):
                    objects.add(objekt)
        
        return objects

    def AddElement(self, element):
        """This method takes a given element and adds it to the quadtree.
 The quadtree rearranges itself if the element unbalances it"""
        self._partition.AddElement(element)

class Partition():
    """This class is a helper struct to QuadTree by storing the rect size of the
 partition. It also stores the gui objects inside this partition"""
    def __init__(self, x, y, width, height, parent=None):
        self._elements = set()
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._subPartitions = None
        self._parent = parent

    @property
    def Elements(self):
        return self._elements

    def AddElement(self, element):
        rendComponent = element.GetComponent('Render')
        rendComponent.QuadPartition = self
        Log.LogMessage("Adding element to the quadtree")
        self._elements.add(rendComponent)
        if self._subPartitions == None:
            if len(self._elements) > QuadTree.MAXELEMENTS:
                self.Subdivide()
        else:
            for partition in self._subPartitions:
                if partition.Collide(rendComponent):
                    partition.AddElement(rendComponent)

    @property
    def Parent(self):
        return self._parent
    
    def UpdatePartition(self, checkElements = False):
        if not checkElements:
            if self._subPartitions == None:
                for element in self._elements:
                    if not self.Collide(element) and self.Parent  != None:
                        self.Parent.UpdatePartition(True)
                        self._elements.remove(element)
            else:
                for partition in self._subPartitions:
                    partition.Update()
        #One of the sub partitions said that we need to check the our elements
        else:
             for element in self._elements:
                 if self.Collide(element):
                     #This will appropriate them to the appropriate subpartition
                     self.AddElement(element)
                 else:
                      self.Parent.UpdatePartition(True)
                      self._elements.remove(element)
                

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
        self._subPartitions[0] = Partition(self.X, self.Y, self.Width / 2,
                                           self.Height / 2, self)
        self._subPartitions[1] = Partition(self.X + (self.Width / 2),
                                           self.Y, self.Width / 2,
                                           self.Height / 2, self)
        self._subPartitions[2] = Partition(self.X, self.Y + (self.Height / 2),
                                           self.Width / 2,
                                           self.Height / 2, self)
        self._subPartitions[3] = Partition(self.X + (self.Width / 2),
                                           self.Y + (self.Height / 2),
                                           self.Width / 2,
                                           self.Height / 2, self)
        for element in self._elements:
            for partition in self._subPartitions:
                if partitiion.Collide(element):
                    partition.AddElement(element)
                

    def Collide(self, renderComponent):
        """This method takes a Object and figures if it collides within this Partition"""
        rect = pygame.Rect(self.X, self.Y, self.Width, self.Height)
        if rect.colliderect(renderComponent.WorldRect.Rect):
            return True
        return False

    def CollideRect(self, rect, partitionList):
        selfRect = pygame.Rect(self.X, self.Y, self.Width, self.Height)
        if selfRect.colliderect(rect):
            if self._subPartitions == None:
                partitionList.append(self)
            else:
                for partition in self._subPartitions:
                    partition.CollideRect(rect, partitionList)

                

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

    

    

    
    
