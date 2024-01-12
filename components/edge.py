import pygame
from components.component import Component


class Edge(Component):
    delta_tL = 150  # timesteps
    delta_tI = 15   # timesteps
    def __init__(self, start_node, end_node, is_inter, time=0):
        super(Edge, self).__init__(time=time)
        self.start_node = start_node
        self.end_node = end_node
        self.is_inter = is_inter
        self.delta_t = Edge.delta_tI if is_inter else Edge.delta_tL
        if start_node.inter is end_node.inter and not is_inter:
            raise AssertionError("Edge connects nodes internally but is_inter is False.")
        if start_node.inter is end_node.inter and not is_inter:
            raise AssertionError("Edge connects nodes from different intersections but is_inter is True.")
        self.set_color()

    def __eq__(self, other):
        return self.start_node == other.start_node and self.end_node == other.end_node
    
    def __str__(self):
        return 'from | ' + str(self.start_node) + '\nto | ' + str(self.end_node)
    
    def set_color(self):
        self.color = pygame.color.Color(255, 255, 255)
    
    def blit(self, screen):
        pygame.draw.line(screen, self.color, self.start_node.loc, self.end_node.loc, 3)
    
    def update(self, screen):
        if screen is not None:
            self.blit(screen)
        self.time += 1