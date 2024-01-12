import pygame
from pygame.sprite import Sprite
from components.methods.methods import *

__all__ = ['Component', 'Intersection', 'Node', 'Edge', 'Graph']


class Component(Sprite):
    """
    Base class for all components needed in the Congestion Control Simulation.
    """
    # Static variables
    # (i, j) : i = distance from top, j = distance from left
    tup_dir_dict = {'E':(0,1), 'N':(-1,0), 'W':(0,-1), 'S':(1,0)}
    op_dir_dict = {'E':'W', 'N':'S', 'W':'E', 'S':'N'}
    lt_dir_dict = {'E':'S', 'N':'E', 'W':'N', 'S':'W'}
    rt_dir_dict = {'E':'N', 'N':'W', 'W':'S', 'S':'E'}

    def __init__(self, time=0):
        super(Component, self).__init__()
        self.time = time
        self.init_time = time

    def set_image(self, path=None):
        """
        Sets display image and location.
        """
        if path is not None:
            self.image = pygame.image.load(path)
            self.display_image = self.image
            self.width = self.image.get_width()
            self.height = self.image.get_height()
        self.rect = center_rect(self)
        self.mask = pygame.mask.from_surface(self.display_image)

    def blit(self, screen):
        pass
    
    def step(self, action=None, screen=None):
        self.time += 1
        if screen is not None:
            self.blit(screen)
