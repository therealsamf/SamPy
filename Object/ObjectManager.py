#ObjectManager.py

from .. import Log
from . import Object
from . import CameraComponent
from . import Component
from .. import Event
from .. import Renderer

import xml.etree.ElementTree as ET
import os, importlib, sys, inspect

ObjectCreatedType = Event.GetType('ObjectCreated')

class ObjectManager():
    gObjectManager = None
    def __init__(self, logic):
        self._objects = set()
        self._objectFactory = None
        self._camera = None
        self._namedObjects = dict()
        if ObjectManager.gObjectManager == None:
            ObjectManager.gObjectManager = self
        self._logicPointer = logic

    @property
    def NamedObjects(self):
        return self._namedObjects

    def GetObjectsFromName(self, name):
        for item in self.NamedObjects:
            Log.LogMessage("Item = " + item)
        if name in self.NamedObjects:
            return self.NamedObjects[name]
        return None

    def Initialize(self):
        Log.LogMessage("Initializing ObjectManager")

        Log.LogMessage("Creating ObjectFactory")
        self._objectFactory = ObjectFactory(self)
        if (self._objectFactory == None):
            Log.LogError("Failure to create ObjectFactory!")
            return False

        if not self._objectFactory.Initialize():
            Log.LogError("Object Factory failed to initialize!")
            return False                

        self._logicPointer._enginePointer.EventManager.RegisterDelegate(
            ObjectCreatedType, self.ObjectCreatedDelegate)
        return True

    def CreateCamera(self):
        """This method just creates a simple camera object with the camera 
component. This is only used when we're not loading an actual level"""
        camera = Object.Object()

        """The way the camera component is set up, all we need to do
        is give the camera object a transform component
        and then give the object the camera component and make sure that
        the cameracomponent's Initialize method gets called"""
        
        cComponent = CameraComponent.CameraComponent(
            camera)
        #declare the xml root node for the transform component
        transformXML = None

        #grab the screen dimensions from the Renderer Module
        (sWidth, sHeight) = Renderer.Renderer.SCREEN_DIMENSIONS
        
        #Define the xml string to pass to the transformcomponent
        nextLine = os.linesep #Make sure we use the right '\n' character
        transformString = "<?xml version='1.0'?>" + nextLine + \
                                          "<transform>" + nextLine + \
                                          "<x>" + str(sWidth / 2) + \
                                          "</x>" + nextLine + "<y>" + \
                                          str(sHeight / 2) + "</y>" + nextLine \
                                          + "<z>" + str(0) + "</z>" + nextLine + \
                                          "<rotation>" + str(0) + \
                                          "</rotation>" + nextLine + "<scale>" \
                                          + str(1) + "</scale>" + nextLine + \
                                          "</transform>"

        """Convert the string to an xml element, load the component, then
add it to the camera with the key 'Transform'"""
        transformXML = ET.fromstring(transformString)
        transformComponent = Component.TransformComponent(camera)
        transformComponent.Load(transformXML)
        camera.AddComponent("transform", transformComponent)

        """Add the camera component. The initialize component on the
cameraComponent must be called before the main loop!"""        
        camera.AddComponent('camera', cComponent)

        self._camera = camera

    def LoadObjects(self, AbsoluteFilepath):
        """This method is for loading just objects that come in an XML file"""
        #Check to make sure it's an XML file
        filename = os.path.split(AbsoluteFilepath)[1]
        fName, ext = os.path.splitext(filename)
        if (ext != '.xml'):
            return False

        else:
            tree = ET.parse(AbsoluteFilepath)
            root = tree.getroot()
            """Iterate through every child in the root
each child should be an object"""            
            for child in root:
                objekt = self.ObjectFactory.CreateObjectFromXML(child)
                self._objects.add(objekt)
        
    def ObjectDestroyedDelegate(self, EventData):
        pass

    def ObjectCreatedDelegate(self, EventData):        
        self._logicPointer.AddObjectToQuadTree(EventData.Object)
        

    def InitializeObjects(self):
        self._camera.Initialize()
        for object in self._objects:
            if not object.Initialize():
                """If I actually start to see these errors, I'll have to find
                a way to identify the offending object"""
                Log.LogError("Object couldn't initialize!")
        return True

    def Update(self, deltaMilliseconds):
        for object in self._objects:
            if (not object.Asleep):
                object.Update(deltaMilliseconds)


    @property
    def ObjectFactory(self):
        return self._objectFactory
        

class ObjectFactory():
    defaultComponentDirectory = os.path.dirname(os.path.abspath(__file__))
    guiComponentDirectory = os.path.join(os.path.dirname(
        os.path.abspath(__file__)),
                                         '../', 'GUI')      
    def __init__(self, Manager):
        self._mgrPointer = Manager
        self._componentClasses = dict()
        self._EventManager = self._mgrPointer._logicPointer._enginePointer.EventManager
        if (self._EventManager == None):
            Log.LogError('Failure to retrieve the EventManager by the' + \
                           ' Object factory')
            

    def Initialize(self):
        self.LoadComponentClasses()
        self.LoadComponentClasses(self.defaultComponentDirectory)
        self.LoadComponentClasses(self.guiComponentDirectory)
        return True

    def CreateObjectFromXML(self, XMLElement):
        """This method loads an Object by all the components in the passed
XML Element"""
        objekt = Object.Object() #Empty object        
        Components = [] #I thought about making this a set, but        
        #some objects should have many script components, which Idk if
        #they would conflict in a set

        Log.LogMessage("Beginning to load object")
        for child in XMLElement:
            Log.LogMessage("Child.tag = " + child.tag)
            if child.tag.lower() in self._componentClasses:
                klass = self._componentClasses[child.tag.lower()]
                comp = klass(objekt)
                comp.Load(child)
                Components.append(comp)
            else:
                Log.LogError("Can't find component: " + child.tag.lower())

        for comp in Components:
            objekt.AddComponent(comp.name.lower(), comp)

        #Construct the eventdata and queue an event
        evtData = Event.Event.ObjectCreatedData(objekt)
        self._EventManager.QueueEvent(Event.Event.Event(ObjectCreatedType,
                                                        evtData))

        #See if the object is named and add it to the manager if it is
        if objekt.Name != None:
            if not objekt.Name in self._mgrPointer.NamedObjects:
                self._mgrPointer.NamedObjects[objekt.Name] = set()
            self._mgrPointer.NamedObjects[objekt.Name].add(objekt)

        return objekt                            

    def CreateObjectFromEventData(self, EventData):
        """This method attempts to create an object from just event data.
This event data is going to have to be indepth"""
        return None

    def LoadComponentClasses(self, path = None):
        if (path == None):
            currentPath = os.path.abspath(".")
        else:
            currentPath = path
        files = os.listdir(currentPath)
        Log.LogMessage("Beginning to load ComponentClasses")

        for File in files:
            filename, extension = os.path.splitext(File)
            if (extension == ".py") and \
            (filename.lower().find("component") != -1) and \
            (filename.lower().find('#') == -1):
                Log.LogMessage("Attempting to import file: " + File)
                loaderModule = None
                try:
                    loaderModule = importlib.import_module('.' + filename,
                                                       __package__)
                except ImportError:
                    try:
                        from .. import GUI
                        loaderModule = importlib.import_module('.' + filename,
                                                               GUI.__package__)
                    except ImportError:
                        raise
                if loaderModule == None:
                    raise ImportError("Failure to load module correctly")
                classes = inspect.getmembers(loaderModule, inspect.isclass)
                for (kname, item) in classes:
                    Log.LogMessage('Name of current item in ' + \
                                   'file is ' + str(item))
                    if (issubclass(item, Component.Component)):
                        loader = item
                        name = loader.name.lower()
                        Log.LogMessage('Name of component being ' + \
                                       'loaded ' + name)
                        self._componentClasses[name] = loader
                    else:
                        Log.LogMessage(str(item.__class__) + ' is not' + \
                                       ' a subclass of Component')


    def AddComponentClass(self, klass):
        if klass.name.lower() not in self._componentClasses:
            self._componentClasses[klass.name.lower()] = klass


    
