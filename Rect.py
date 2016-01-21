
#Rect.py

import pygame

class Rectangle():
    def __init__(self, **kwargs):
        rect = kwargs.get('rect', None)
        if (rect == None):
            x = kwargs.get('x', 0)
            y = kwargs.get('y', 0)
            w = kwargs.get('width', 0)
            w = kwargs.get('w', w)
            h = kwargs.get('h', 0)
            h = kwargs.get('height', h)
            self._rect = pygame.Rect(x, y, w, h)            
        else:
            self._rect = rect

    @property
    def x(self):
        return self._rect.x
    @property
    def y(self):
        return self._rect.y
    @property
    def Rect(self):
        return self._rect

    @property
    def h(self):
        return self._rect.h

    @property
    def w(self):
        return self._rect.w

    @property
    def width(self):
        return self._rect.w
    @property
    def height(self):
        return self._rect.h
    
    def __eq__(self, other):
        if (other.__class__ != Rectangle):
            return False
        else:
            return self.h == other.h and \
                self.w == other.w and \
                self.x == other.x and \
                self.y == other.y


    def __hash__(self):
        return 1 * self._rect.x + 2 * self._rect.y + 3 * self._rect.width + \
            4 * self._rect.height

    def __str__(self):
        return "Rect(" + str(self.Rect.x) + ", " + str(self.Rect.y) + \
            ", " + str(self.Rect.w) + ", " + str(self.Rect.h)

    def Load(self, XMLElement):
        """This method is to load the rect from an xml element"""
        x = int(XMLElement.find('x').text)
        y = int(XMLElement.find('y').text)
        w = int(XMLElement.find('w').text)
        h = int(XMLElement.find('h').text)
        self._rect = pygame.Rect(x, y, w, h)
    
