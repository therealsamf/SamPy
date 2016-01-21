#ImageLoader.py

from . import ResourceCache
from .. import Log

import pygame, os
from pygame.locals import *

class ImageLoader(ResourceCache.Loader):
    def __init__(self):
        super().__init__()

    def Load(self, AbsolutePath):
        Log.LogMessage("ImageLoader received path: " + \
                       AbsolutePath)
        filepath, filename = os.path.split(AbsolutePath)
        filename, extension = os.path.splitext(filename)
        Log.LogMessage("Exension for " + filename.join(extension)  + " = " + \
                       extension)

        surface = None
        if extension in ['.png', '.jpg', '.tga']:
            Log.LogMessage("ImageLoader acknowledges " + filename + extension + \
                           " is an extended image filetype")
            if (pygame.image.get_extended()):
                Log.LogMessage("Attempting to load " + filename + extension + \
                               " with pygame.image.load")
                surface = pygame.image.load(AbsolutePath)
            else:
                Log.LogError("Pygame can't load extended filetypes!")

        else:
            surface = pygame.image.load(AbsolutePath)

        return surface
                    


    def GetExtension(self):
        if (pygame.image.get_extended()):
            return ['.png', '.bmp', '.jpg', '.tga']
        else:
            return ['.bmp']
