#ThemeComponent.py

from .. import Object
from .. import Resource

import tinycss

class ThemeComponent(Object.Component.Component):
    name = 'Theme'
    def __init__(self, Object):
        super().__init__(Object)
        self._css = None

    def Initialize(self):
        self._objectPtr.Asleep = True

        return True


    def Load(self, XMLElement):
        self._filename = XMLElement.find('filename').text
        self._css = \
                    Resource.ResourceCache. \
                    ResourceCache.gResourceCache.GetResource(
            self._filename)
        self._objectPtr.Name = self._filename

    def GetProperty(self, selector, Property):
        rules = self._css.rules
        ruleset = None
        for item in rules:
            if isinstance(item, tinycss.css21.RuleSet) and ruleset == None:
                currentSelector = ""
                for token in item.selector:
                    if token.value != ',' and token.value != ' ':
                        currentSelector += token.value
                    else:
                        currentSelector = ""
                    if currentSelector != "" and \
                       currentSelector == selector:
                        ruleset = item
                        break

        if ruleset != None:
            for item in ruleset.declarations:
                if item.name == Property:
                    return item.value

            
            periodIndex = selector.find('.')
            if periodIndex != -1:
                parent = selector[0:periodIndex]
                return self.GetProperty(parent, Property)
            
        return None
        

        

    
    
