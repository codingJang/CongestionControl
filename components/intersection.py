import pygame
import numpy as np
from components.component import Component
from components.methods.methods import center_blit, center_rect, to_vector2

class Intersection(Component):
    """
    Intersection class.
    Includes coordinates i, j as member variables, == operation and + operation.
    """
    traffic_light = np.zeros((8, 4, 2), dtype=bool)
    idx_1 = {'E':0, 'N':1, 'W':2, 'S':3}
    idx_2 = {'lt':0, 'gs':1}
    traffic_light[0, idx_1['E'], idx_2['gs']] = True
    traffic_light[0, idx_1['W'], idx_2['gs']] = True
    traffic_light[1, idx_1['E'], idx_2['lt']] = True
    traffic_light[1, idx_1['W'], idx_2['lt']] = True
    traffic_light[2, idx_1['N'], idx_2['gs']] = True
    traffic_light[2, idx_1['S'], idx_2['gs']] = True
    traffic_light[3, idx_1['N'], idx_2['lt']] = True
    traffic_light[3, idx_1['S'], idx_2['lt']] = True
    traffic_light[4, idx_1['E'], idx_2['gs']] = True
    traffic_light[4, idx_1['E'], idx_2['lt']] = True
    traffic_light[5, idx_1['N'], idx_2['gs']] = True
    traffic_light[5, idx_1['N'], idx_2['lt']] = True
    traffic_light[6, idx_1['W'], idx_2['gs']] = True
    traffic_light[6, idx_1['W'], idx_2['lt']] = True
    traffic_light[7, idx_1['S'], idx_2['gs']] = True
    traffic_light[7, idx_1['S'], idx_2['lt']] = True

    def __init__(self, i, j, time=0):
        """
        Initializes Intersection object.
        :param i: number of blocks counted from top to bottom.
        :param j: number of blocks counted from left to right.
        """
        super(Intersection, self).__init__(time=time)
        self.i = i
        self.j = j
        self.mode = None
        # loc is a pygame.math.Vector2 object, with loc.x=c*j and loc.y=c*i for some c.
        self.loc = to_vector2((i, j))
        self.set_image('images/intersection.png')
        self.set_text('fonts/NanumGothic.ttf')

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j
    
    def __add__(self, other):
        """
        Adds tuples of the form (int, int) to get Intersection with new coordinates.
        :param other: tuple of the form (int, int)
        """
        if isinstance(other[0], int) and isinstance(other[1], int):
            return Intersection(self.i + other[0], self.j + other[1])
        else:
            raise ValueError('The right hand side should be a tuple of the form (int, int).')
    
    def __str__(self):
        return f"Intersection at: i={self.i}, j={self.j}"

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
    
    def set_text(self, path=None):
        self.font = pygame.font.Font(path, 10)
        self.color = (255, 255, 255)
        self.display_text = self.font.render(f'{self.mode}', True, self.color)
    
    def update_text(self):
        self.display_text = self.font.render(f'{self.mode}', True, self.color)
        
    def blit(self, screen):
        self.update_text()
        center_blit(self.display_image, self.loc, screen)
        center_blit(self.display_text, self.loc, screen)

    def step(self, action, screen=None):
        if action is None:
            self.mode = (self.time % 240) // 30
        else:
            self.mode = action
        if screen is not None:
            self.blit(screen)
        self.time += 1
