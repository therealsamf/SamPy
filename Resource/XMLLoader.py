#XMLLoader.py

from .. import Log
from . import ResourceCache

import os
import xml.etree.ElementTree as ET

class XMLLoader(ResourceCache.Loader):
    def __init__(self):
        super().__init__()

    def Load(self, AbsolutePath):
        directoryPath, filename = os.path.split(AbsolutePath)
        filename, extension = os.path.splitext(filename)
        if extension == '.xml':
            root = ET.parse(AbsolutePath)
            return root
        return None
    

    def GetExtension(self):
        return ['.xml']
