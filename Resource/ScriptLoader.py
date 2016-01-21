#ScriptLoader.py


from .. import Log
from . import ResourceCache
import os, importlib

class ScriptLoader(ResourceCache.Loader):
    def __init__(self):
        super().__init__()
        pass

    def Load(self, AbsolutePath):
        from .. import Object
        try:
            module = None
            directorypath, fullname = os.path.split(AbsolutePath)
            filename, extension = os.path.splitext(fullname)
            if extension == '.py':
                if filename.lower().find('component') != -1:
                    try:
                        import sys
                        sys.path.append(directorypath)
                        
                        module = importlib.__import__(filename)
                        module = module.CreateComponent(__import__(
                            __name__.split('.')[0]))
                    except:
                        import traceback
                        traceback.print_exc()
                        
                    """
                    try:
                        print(fullname)
                        module = importlib.import_module('.' + fullname,
                                                         __package__)
                    except ImportError as e:
                        import traceback
                        traceback.print_exc()
"""
                        
            return module
        except BaseException as e:
            raise Object.Object.SamError(e.__traceback__)

    def GetExtension(self):
        return ['.py']
