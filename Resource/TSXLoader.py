#TSXLoader.py

"""This class is used for loading Tileset objects, that are found
in tilemap objects in the Tiled Editor"""

from . import ResourceCache

class TSXLoader(ResourceCache.Loader):
    def __init__(self):
        super().__init__()

    def GetExtension(self):
        return [".tsx"]

    def Load(self, AbsoluteFilename):
        """This method loads tilesets"""
        #Test to see if the parameter is an XMLElement or
        #a filename

        #This should implement an xml parser to parse through the
        #xml file. It should load the tile images into the ResourceCache
        
