#Object.py

from .. import Log

class Object():
    def __init__(self):
        self._name = None
        self._componentMap = dict()
        self._asleep = False

    @property
    def Name(self):
        return self._name
    
    @Name.setter
    def Name(self, value):
        if type(value) == str:
            self._name = value

    def AddComponent(self, key, component):
        self._componentMap[key.lower()] = component

    def Initialize(self):
        """This method initializes all of its components"""
        success = True
        failures = list()
        reps = 0
        for component in self._componentMap:
            failures.append(component)
        while len(failures) > 0 and reps < 10:
            size = len(failures)
            for i in range(size):
                component = failures.pop()
                try:
                    failure = self._componentMap[component].Initialize()
                    if not failure:
                        Log.LogError("Component " + component + \
                                     " failed to initialize!")
                        failures.insert(0, component)
                except SamError as e:
                    print(e.Value)
                    raise
                except BaseException:
                    failures.insert(0, component)

            reps += 1
                    
              
        return success

    def GetComponent(self, key):       
        if (type(key) == str and key.lower() in self._componentMap):
            return self._componentMap[key.lower()]
        elif type(key) != str:
            for name in self._componentMap:
                if issubclass(self._componentMap[name].__class__, key):
                    return self._componentMap[name]

        return None

    def Update(self, deltaMilliseconds):
        for component in self._componentMap:
            self._componentMap[component].Update(deltaMilliseconds)

    def CheckComponent(self, ComponentName):
        if (not ComponentName.lower() in self._componentMap):
            return False
        return True

    @property
    def Asleep(self):
        return self._asleep

    @Asleep.setter
    def Asleep(self, value):
        if (type(value) == bool):
             self._asleep = value
             
        
class SamError(Exception):
    def __init__(self, value):
        self._value = value

    @property
    def Value(self):
        return self._value

    @Value.setter
    def Value(self, value):
        self._value = value
