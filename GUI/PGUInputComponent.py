from . import PGUTextBoxComponent
import pgu.gui as gui

class PGUInputComponent(PGUTextBoxComponent.PGUTextBoxComponent):
    name = 'PGUInput'
    def __init__(self, objectPointer):
        PGUTextBoxComponent.PGUTextBoxComponent.__init__(self, objectPointer)

    def Load(self, XMLDoc):
        width = int(XMLDoc.find('width').text)
        value = XMLDoc.find('value').text
        self._width = width
        self._widget = gui.Input(value = value, width = self._width)
