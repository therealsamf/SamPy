#Debug.py

import pygame


"""All of these functions should only be called after
everything has been initialized. This will crash and burn if pygame
hasn't been initialized or the screen hasn't been created yet"""

#Predifined Colors:
BLUE = pygame.Color(0, 0, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)

#Predefined variables
LINE_THICKNESS = 3

def DrawRect(rect):
    if pygame.display.get_init():
        screen = pygame.display.get_surface()
        pygame.display.update(pygame.draw.rect(screen, BLUE, rect,
                                               LINE_THICKNESS))
    else:
        return

def DrawLine(point1, point2):
    if pygame.display.get_init():
        screen = pygame.display.get_surface()
        pygame.display.update(pygame.draw.line(screen, RED, point1, point2,
                                               LINE_THICKNESS))

def DrawCircle(point, radius):
    if pygame.display.get_init():
        screen = pygame.display.get_surface()
        pygame.display.update(pygame.draw.line(screen, GREEN, point, radius,
                                               LINE_THICKNESS))
    
