#Renderer.py

import pygame, math, bisect
from pygame.locals import *

from .. import Log
from .. import Process
from .. import Rect
from .. import Debug

hashRect = Rect.Rectangle

SCREEN_DIMENSIONS = (800, 400)
SCALING_FACTOR = 2.0

class Renderer():
    gRenderer = None
    def __init__(self, gameLogic):
        self._screen = None
        self._updateRects = None
        self._uRects = None
        self._process = None
        self._renders = None
        if (Renderer.gRenderer == None):
            gRenderer = self
        self._logicPointer = gameLogic


    def Initialize(self):
        Log.LogMessage("Initializing Renderer")

        self._updateRects = set()
        self._uRects = list()
        self._renders = RenderTree(root = True)

        Log.LogMessage("Initializing Pygame")
        pygame.init()
        
        Log.LogMessage("Creating screen")
        if (pygame.display.get_init()):
            self._screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
            if (self._screen == None):
                Log.LogError("Failure to create")
                return False
        else:
            Log.LogError("Failure to initialize Pygame correctly!")
            return False

        self._process = RendererProcess(self)
        self._logicPointer.ProcessManager.AttachProcess(self._process)

        from .. import Event
        Event.EventManager.EventManager.gEventManager.RegisterDelegate(
            Event.GetType('ScheduleRender'), self.ScheduleRenderDelegate)
        """
        Event.EventManager.EventManager.gEventManager.RegisterDelegate(
            Event.GetType('AddUpdateRect'), self.AddUpdateRect)
"""
        
        return True

    def ClearUpdateRects(self):
        self._updateRects = set()
        self._uRects = list()

    def GetUpdateRects(self):
        return self._uRects

    def ConvertFromWorldCoor(coor):
        length = 0
        try:
            length = len(coor)
        except TypeError:
            return (0, 0)

        if (length >= 2):
            x = round(coor[0] * SCALING_FACTOR)
            y = round(coor[1] * SCALING_FACTOR)
            return (x, y)

        return (0, 0)

    def ConvertFromPixelCoor(coor):
        length = 0
        try:
            length = len(coor)
        except TypeError:
            Log.LogError("Attempting to convert pixel coordinates without inputting a tuple!")
            return (0, 0)

        if (length >= 2):
            x = coor[0] / SCALING_FACTOR
            y = coor[1] / SCALING_FACTOR
            return (x, y)
        return (0, 0)

    def Render(self, **kwargs):
        surface = kwargs.get('surface', None)
        if (surface == None):
            return
        flip = kwargs.get('flip', False)
        rotations = kwargs.get('rotation', 0.0)
        coor = kwargs.get('coor', (0, 0))
        if (coor[0] % 1 != 0): #this is in world coordinates
            coor = self.ConvertFromWorldCoor(coor)

        area = kwargs.get('area', None)

        surface = pygame.transform.flip(surface, flip, False)
        surface = pygame.transform.rotate(surface, rotations)

        updateRect = self.Screen.blit(surface, coor, area)
        self._updateRects.append(updateRect)

    def ScheduleRender(self, **kwargs):
        surface = kwargs.get('surface', None)
        if (surface == None):
            return
        flip = kwargs.get('flip', False)
        rotations = kwargs.get('rotation', 0.0)
        coor = kwargs.get('coor', (0, 0))
        if (coor[0] % 1 != 0): #this is in world coordinates
            coor = self.ConvertFromWorldCoor(coor)

        area = kwargs.get('area', None)
        if area != None and area.Rect.w != 0 and area.Rect.h != 0:
            surface = surface.subsurface(area.Rect)
        surface = pygame.transform.flip(surface, flip, False)
        surface = pygame.transform.rotate(surface, rotations)
        layer = kwargs.get('layer', 0)
        ID = kwargs.get('ID', 0)

        render = Render.CreateRender(surface, area, coor, layer, ID, rotations)
        self._renders.Insert(render)

    def ScheduleRenderDelegate(self, data):
        self.ScheduleRender(surface = data.Surface,
                            flip = data.Flip,
                            coor = data.Coor,
                            layer = data.Layer,
                            area = data.Area,
                            rotation = data.Rotation,
                            ID = data.ID)

    def AddUpateRectDelegate(self, data):
        Log.LogMessage("Rect added: " + data.Rect)
        self.AddUpateRect(data.Rect)
                            

    @property
    def Renders(self):
        return self._renders.ToList()

    @property
    def Screen(self):
        return self._screen

    def AddUpdateRect(self, rect):
        if rect.Rect == None:
            return
        if not rect in self._updateRects and rect.Rect.w != 0 and \
           rect.Rect.h != 0:
            Log.LogMessage("Adding rect " + str(rect.Rect) + " to UpdateRects")
            self._updateRects.add(rect)
            self._uRects.append(rect.Rect)

    def ClearRenders(self):
        self._renders.Clear()
        
        


class RendererProcess(Process.Process.Process):
    def toString(self):
        return 'RenderProcess'
    
    def __init__(self, renderPointer):
        super().__init__()
        self._lastUpdate = 0
        self._frameRate = 1.0 / 60
        self._updateRects = list()
        self._renderPointer = renderPointer

    def Update(self, deltaMilliseconds):
        if (deltaMilliseconds + self._lastUpdate > (1000 * self._frameRate)):
            renderList = self._renderPointer.Renders
            Log.LogMessage("RenderProcessUpdate" + " " + \
                           str(len(renderList)) + \
                           " renders")
            for render in renderList:
                Log.LogMessage("RenderSurface = " + str(render.Surface))
                self._renderPointer.Screen.blit(render.Surface, render.Coor)
            Log.LogMessage("Number of update rects: " + \
                           str(len(self._renderPointer.GetUpdateRects())))

            pygame.display.update(self._renderPointer.GetUpdateRects())
            #pygame.display.flip()
            self._renderPointer.ClearUpdateRects()
            self._renderPointer.ClearRenders()
            self._lastUpdate = 0
        else:
            self._lastUpdate += deltaMilliseconds


class Render():
    RecycledRenders = []
    def CreateRender(surface, area, coor, layer, ID, rotation, override=True):
        """This method checks to see if we can reuse old render objects. 
This in theory limits the amount of work for the garbage collector"""

        #Check to see if we have any old renders
        if len(Render.RecycledRenders) == 0:
            #Create a new one
            return Render(surface, area, coor, layer, ID, rotation, override)
        else:
            #Get the newest old render
            oldRender = Render.RecycledRenders.pop()
            #Basically call a fake '__init__' method on the old render
            oldRender.__init__(surface, area, coor, layer, ID, rotation,
                               override)
            return oldRender

    def Recycle(oldRender):
        Render.RecycledRenders.append(oldRender)
        
    def __init__(self, surface, area, coor, layer, ID, rotation,
                 override=True):
        self._surface = surface
        self._area = area
        self._coor = coor
        self._layer = layer
        self._ID = ID
        self._rotation = rotation
        self._left = None
        self._right = None
        self._override = override

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
    def Coor(self):
        return self._coor

    @property
    def Area(self):
        return self._area
    @property
    def Surface(self):
        return self._surface

    @property
    def Left(self):
        return self._left
    @property
    def Right(self):
        return self._right

    @Left.setter
    def Left(self, value):
        self._left = value

    @Right.setter
    def Right(self, value):
        self._right = value

    @property
    def Override(self):
        return self._override


    def __hash__(self):
        rect = self.Area
        hashNum = 0
        hashNum = 1 * rect.w + 2 * rect.h

        return self.ID * self.Layer

    def __eq__(self, other):
        if other.__class__ != self.__class__:
            return False
        else:
            return self.__hash__() == other.__hash__()

    """None of these functions have type checking because they should only
be compared to themselves"""
    def __gt__(self, other):
        if self.Layer != other.Layer:
            return self.Layer > other.Layer
        else:
            return self.__hash__() > other.__hash__()
        
    def __lt__(self, other):
        if self.Layer != other.Layer:
            return self.Layer < other.Layer
        else:
            return self.__hash__() < other.__hash__()
        
    def __ge__(self, other):
        if self.Layer != other.Layer:
            return self.Layer >= other.Layer
        else:
            return self.__hash__() >= other.__hash__()
        
    def __le__(self, other):
         if self.Layer != other.Layer:
            return self.Layer <= other.Layer
         else:
            return self.__hash__() <= other.__hash__()


class RenderTree():
    RenderTreeRecycle = []
    def CreateRenderTree(render):
        if len(RenderTree.RenderTreeRecycle) == 0:
            return RenderTree(False, render)
        else:
            oldRenderTree = RenderTree.RenderTreeRecycle.pop()
            """This assumes that this render is clean and won't mess things
up when we set it"""
            oldRenderTree.__init__(False, render)
            return oldRenderTree
    def Recycle(renderTree):
        RenderTree.RenderTreeRecycle.append(renderTree)
    def __init__(self, root = False, render = None):
        self._node = render
        self._height = 0 #?
        self._balance = 0
        self._root = root

    def Insert(self, render):
        if self.Node == None:
            self.Node = render
        elif render < self.Node:
            if self.Node.Left == None:
                self.Node.Left = RenderTree.CreateRenderTree(render)
            else:
                self.Node.Left.Insert(render)

        elif render > self.Node:
            if self.Node.Right == None:
                self.Node.Right = RenderTree.CreateRenderTree(render)
            else:
                self.Node.Right.Insert(render)
        else: #render == self.Node
            Log.LogMessage("ID of this render ==" + str(render.ID))
            Log.LogMessage("ID of this node == " + str(self.Node.ID))
            """We've got a render with the same layer and ID"""
            if self.Node.Override:
                leftSub = self.Node.Left
                rightSub = self.Node.Right
                self.Node = render
                self.Node.Left = leftSub
                self.Node.Right = rightSub

        self.Rebalance()
        
    def Rebalance(self):
        self.UpdateHeight(recursive = False)
        self.UpdateBalances(False)

        while self.Balance < -1 or self.Balance > 1:
            #Leftsubtree is larger than right subtree
            if self.Balance > 1:
                if self.Node.Left and self.Node.Left.Balance < 0:
                    self.Node.Left.RotateLeft()
                    self.UpdateHeight()
                    self.UpdateBalances()
                self.RotateRight()
                self.UpdateHeight()
                self.UpdateBalances()
            if self.Balance < -1:
                if self.Node.Right and self.Node.Right.Balance > 0:
                    self.Node.Right.RotateRight()
                    self.UpdateHeight()
                    self.UpdateBalances()
                self.RotateLeft()
                self.UpdateHeight()
                self.UpdateBalances()

    def RotateLeft(self):
        new_root = None
        new_root_sub = None
        if self.Node:
            new_root = self.Node.Right
        if new_root and new_root.Node.Left:
            new_root_sub = new_root.Node.Left
        old_root = self.Node

        self.Node = new_root.Node
        old_root.Right = new_root_sub

        new_root.Node.Left = RenderTree.CreateRenderTree(old_root)
    

    def RotateRight(self):
        """Hopefully this only gets called if there are three nodes to 
be rotated"""
        new_root = None
        new_root_sub = None
        if self.Node:
            new_root = self.Node.Left
        if new_root and new_root.Node.Right:
            new_root_sub = new_root.Node.Right
        old_root = self.Node

        self.Node = new_root.Node
        old_root.Left = new_root_sub
        new_root.Node.Right = RenderTree.CreateRenderTree(old_root)

    def UpdateHeight(self, recursive = True):
        if self.Node != None:
            if recursive:
                if self.Node.Left != None:
                    self.Node.Left.UpdateHeight()
                if self.Node.Right != None:
                    self.Node.Right.UpdateHeight()
            rightHeight = -1
            leftHeight = -1
            if self.Node.Right:
                rightHeight = self.Node.Right.Height
            if self.Node.Left:
                leftHeight = self.Node.Left.Height
            self._height = 1 + max(rightHeight, leftHeight)
        else:
            self._height = -1

    def UpdateBalances(self, recursive = True):
        """
Calculate Tree Balance Factor:

the balance factor is calculated as follows:
balance = height(left subtree) - height(rightsubtree)
"""
        if self.Node:
            if recursive:
                if self.Node.Left:
                    self.Node.Left.UpdateBalances()
                if self.Node.Right:
                    self.Node.Right.UpdateBalances()
            rightHeight = -1
            leftHeight = -1
            if self.Node.Right:
                rightHeight = self.Node.Right.Height
            if self.Node.Left:
                leftHeight = self.Node.Left.Height
            self._balance = leftHeight - rightHeight
        else:
            self._balance = 0
                

    @property
    def Height(self):
        return self._height
    @property
    def Balance(self):
        return self._balance

    @property
    def Node(self):
        return self._node

    @Node.setter
    def Node(self, value):
        if not isinstance(value, Render) and not value == None:
            raise ValueError
        """This method is not to be used outside of the class"""
        self._node = value


    def ToList(self):
        result = []
        if self.Node:
            if self.Node.Left:
                result.extend(self.Node.Left.ToList())
            result.append(self.Node)
            if self.Node.Right:
                result.extend(self.Node.Right.ToList())
        return result

    def Clear(self):
        if self.Node:
            
            if self.Node.Left:
                self.Node.Left.Clear()
            if self.Node.Right:
                self.Node.Right.Clear()
            Render.Recycle(self.Node)

            self.Node = None #This shouldn't break anything...
        """Check to make sure we're putting the root back into the pool of
        recycled 
        """
        
        if not self._root:
            RenderTree.Recycle(self)
            
    
"""This class is obsolete!"""        
class RenderList():
    def __init__(self):
        self._rList = []
        self._rSet = set()

    def Insert(self, render):
        Log.LogMessage("Number of items in RenderSet: " + \
                       str(len(self._rSet)))
        Log.LogMessage("RenderSurface = " + str(render.Surface))
        if render in self._rSet:
            Log.LogMessage("Render skipped")
            return
        self._rSet.add(render)
        if len(self._rList) == 0:
            self._rList.append(render)
        else:
            self.Insertb(render, 0, len(self._rList) - 1)
    def clear(self):
        self._rList = list()
        self._rSet = set()

    def Insertb(self, render, left, right):
        Log.LogMessage("Left = " + str(left))
        Log.LogMessage("Right = " + str(right))
        if left >=  right:
            if self._rList[left] < render:
                self._rList.insert(left + 1, render)
            elif self._rList[left] > render:
                self._rList.insert(left, render)
            else:
                if self._rList[left].ID == render.ID:
                    self._rList[left] = render
        else:
            mid = left + math.floor((right - left) / 2)
            Log.LogMessage("Mid Index = " + str(mid))
            if self._rList[mid] < render:
                self.Insertb(render, mid + 1, right)
            elif self._rList[mid] > render:
                self.Insertb(render, left, mid - 1)
            else:
                if self._rList[mid].ID == render.ID:
                    self._rList[mid] = render
                    

    def __iter__(self):
        for item in self._rList:
            yield item

    def __len__(self):
        return len(self._rList)


