#TMXLoader.py

from . import ResourceCache
from .. import Log
import tmx, os

class TMXLoader(ResourceCache.Loader):
    """This class uses the simple TMX library to load a tilemap file into
the resource cache. It then will also load all the images and tilesets into the 
resourcecache that are not already there"""
    def __init__(self):
        self._tilemap = None

    def GetExtension(self):
        return [".tmx"]

    def Load(self, AbsoluteFilepath):
        filename = os.path.split(AbsoluteFilepath)
        #Load the tilemap
        self._tilemap = tmx.TileMap.load(filename)
        TSXLoaderPtr = ResourceCache.ResourceCache.gResourceCache.GetLoader(".tsx")
        if (TSXLoaderPtr == None):
            Log.LogError("Can't load tilemap object without TSXLoader")

        for tileset in self._tilemap.tilesets:
            if tileset.source != None:
                TSXLoaderPtr.Load(tileset.source)

        #If we need to preload objects I guess we should load those?

    
            
    
        
        
        
