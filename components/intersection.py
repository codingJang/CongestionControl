import pygame
from components.component import Component
from components.methods.methods import center_blit, center_rect, to_vector2

class Intersection(Component):
    """
    Intersection class.
    Includes coordinates i, j as member variables, == operation and + operation.
    """
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
            self.mode = (self.time % 16) // 2
        else:
            self.mode = action
        self.blit(screen)
        super(Intersection, self).step(screen=screen)
