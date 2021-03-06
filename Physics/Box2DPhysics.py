#Box2DPhysics.py

import pypybox2d as box2d
#from box2d import *

from .. import Process as pc
from .. import Log

class Box2DPhysics():
    #Ps = pc.ProcessManager.ProcessManager.gProcessManager
    #Ev = ev.EventManager.EventManager.gEventManager
    def __init__(self, gameLogic):
        self._world = None
        self._process = None
        self._logicPointer = gameLogic

        """We have to import this now, because if we do it at the top it'll give
us an error"""        
        from .. import Engine
        self._enginePointer = Engine.Engine.gEngine

    def Initialize(self, pGravity=(0, -10)):
        Log.LogMessage("Initializing Physics")

        Log.LogMessage("Creating Box2D world")
        self._world = box2d.World(gravity = pGravity)
        if (self._world == None):
            Log.LogError("Creation of the Box2d World failed!")

        Log.LogMessage("Creating PhysicsProcess")
        self._process = PhysicsProcess(self.World)
        if (self._process == None):
            Log.LogError("Creation of the Physics Process failed!")
        self._logicPointer.ProcessManager.AttachProcess(self._process)

        Log.LogMessage("Registering delegate functions with EventManager")
        self._enginePointer.EventManager.RegisterDelegate("ObjectDestroyed",
                                         self.BodyDestroyedDelegate)
        self._enginePointer.EventManager.RegisterDelegate("ObjectCreated",
                                          self.BodyCreatedDelegate)

        return True

    def BodyDestroyedDelegate(self, EventData):
        pass

    def BodyCreatedDelegate(self, EventData):
        pass

    def GetBodiesInRect(self, **kwargs):
        x = kwargs.get('x', 0)
        y = kwargs.get('y', 0)
        width = kwargs.get('width', 0)
        height = kwargs.get('height', 0)
        rect = box2d.AABB((x, y + height), ((x + width), y))
        bodies = set()
        get = self.World.query_aabb(rect)
        return get



        
    #I'm sure I'll be putting more event delegate functions down here eventually

            

    @property
    def World(self):
        return self._world;


class PhysicsProcess(pc.Process.Process):
    def __init__(self, world=None, timeStep=1.0 / 6, vel_iterations = 6,
                 position_iterations = 2):
        pc.Process.Process.__init__(self)
        self._world = world
        self.vel_iters = vel_iterations
        self.pos_iters = position_iterations
        self.time_step = timeStep
        self.lastUpdate = 0

    def Update(self, deltaMilliseconds):
        if (deltaMilliseconds + self.lastUpdate > (self.time_step * 1000)):
            self._world.step(self.time_step, self.vel_iters, self.pos_iters)
            self._world.clear_forces()
            self.lastUpdate = 0
        else:
            self.lastUpdate += deltaMilliseconds

    def toString(self):
        return "PhysicsProcess"
        
            

    
