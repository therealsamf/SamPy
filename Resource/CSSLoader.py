#CSSLoader.py

from . import ResourceCache
import tinycss


class CSSLoader(ResourceCache.Loader):
    def __init__(self):
        super().__init__()

    def Load(self, AbsoluteFilepath):
        parser = tinycss.make_parser('page3')
        stylesheet = parser.parse_stylesheet_file(AbsoluteFilepath)
        return stylesheet

    def GetExtension(self):
        return ['.css']
