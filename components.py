import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2
from methods import *

__all__ = ['Component', 'Intersection', 'Node', 'Graph']


class Component(Sprite):
    """
    Base class for all components needed in the Congestion Control Simulation.
    """
    # Static variables
    # (i, j) : i = distance from top, j = distance from left
    dir_dict = {'E':(0,1), 'N':(-1,0), 'W':(0,-1), 'S':(1,0)}  
    opposite_dir = {'E':'W', 'N':'S', 'W':'E', 'S':'N'}
    turn_left_dir = {'E':'S', 'N':'E', 'W':'N', 'S':'W'}
    turn_right_dir = {'E':'N', 'N':'W', 'W':'S', 'S':'E'}

    def __init__(self):
        super(Component, self).__init__()
        self.display_image = None
        self.loc = None

    def blit(self, screen):
        center_blit(self, screen)


class Intersection(Component):
    """
    Intersection class.
    Includes coordinates member variables, == operation and + operation.
    """
    def __init__(self, i, j):
        """
        Initializes Intersection object.
        :param i: number of blocks counted from top to bottom.
        :param j: number of blocks counted from left to right.
        """
        super(Intersection, self).__init__()
        self.i = i
        self.j = j
        self.loc = to_vector2((i, j))
        self.set_image('images/intersection.png')

    def __eq__(self, other):  # compare coordinates
        return self.i == other.i and self.j == other.j
    
    def __add__(self, other):
        """
        Adds tuples of the form (int, int) to get Intersection with new coordinates.
        """
        return Intersection(self.i + other[0], self.j + other[1])
    
    def __str__(self):
        return f"i={self.i}, j={self.j}"

    def set_image(self, path=None):  # Choose image and set location
        if path is not None:
            self.image = pygame.image.load(path)
            self.display_image = self.image
            self.width = self.image.get_width()
            self.height = self.image.get_height()
        self.rect = center_rect(self)
        self.mask = pygame.mask.from_surface(self.display_image)
        


class Node(Component):
    """
    Node at a given intersection oriented in some direction,
    with bool values for is_incoming and is_fringe.
    """
    def __init__(self, inter, dir, is_incoming, is_fringe):
        super(Node, self).__init__()
        self.inter = inter
        self.dir = dir
        self.is_incoming = is_incoming
        self.is_fringe = is_fringe
        self.set_color()
        self.set_location()
    
    def __eq__(self, other):
        is_eq = True
        is_eq = is_eq and self.inter == other.inter
        is_eq = is_eq and self.dir == other.dir
        is_eq = is_eq and self.is_incoming == other.is_incoming
        is_eq = is_eq and self.is_fringe == other.is_fringe
        return is_eq
    
    def __str__(self):
        return f"i={self.loc.y/240:.2f}, j={self.loc.x/240:.2f}, dir={self.dir}, is_incoming={self.is_incoming}, is_fringe={self.is_fringe}"

    def set_color(self):
        color_value = (255, 0, 0) if self.is_incoming else (0, 0, 255)
        self.color = pygame.color.Color(*color_value)
    
    def set_location(self):
        node_loc = Vector2(self.inter.loc)
        dir_dict = Component.dir_dict
        turn_left_dir = Component.turn_left_dir
        turn_right_dir = Component.turn_right_dir
        node_loc += 0.20 * to_vector2(dir_dict[self.dir])
        if self.is_incoming:
            node_loc += 0.08 * to_vector2(dir_dict[turn_left_dir[self.dir]])
        else:
            node_loc += 0.08 * to_vector2(dir_dict[turn_right_dir[self.dir]])
        self.loc = node_loc

    
    def blit(self, screen):
        pygame.draw.circle(screen, self.color, self.loc, 5, 0)


class Edge(Component):
    delta_tL = 10  # timesteps
    delta_tI = 2   # timesteps
    def __init__(self, start_node, end_node, is_inter):
        super(Edge, self).__init__()
        self.start_node = start_node
        self.end_node = end_node
        self.is_inter = is_inter
        self.delta_t = Edge.delta_tI if is_inter else Edge.delta_tL
        if start_node.inter == end_node.inter and not is_inter:
            raise AssertionError("Edge connects nodes internally but is_inter is False.")
        if start_node.inter == end_node.inter and not is_inter:
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


class Graph(Component):
    def __init__(self, H, L):
        super(Graph, self).__init__()
        self.H = H
        self.L = L
        self.construct_inters()
        self.construct_nodes()
        self.construct_edges()
    
    def construct_inters(self):
        H = self.H
        L = self.L
        self.fringe_inters = []
        self.fringe_inters += [Intersection(0, j) for j in range(1, L+1)]
        self.fringe_inters += [Intersection(H+1, j) for j in range(1, L+1)]
        self.fringe_inters += [Intersection(i, 0) for i in range(1, H+1)]
        self.fringe_inters += [Intersection(i, L+1) for i in range(1, H+1)]
        self.interm_inters = []
        for i in range(1, H+1):
            for j in range(1, L+1):
                self.interm_inters.append(Intersection(i, j))
        self.inters = self.fringe_inters + self.interm_inters
    
    def construct_nodes(self):
        H = self.H
        L = self.L
        self.fringe_nodes = []
        for inter in self.fringe_inters:
            if inter.i == 0:
                self.fringe_nodes.append(Node(inter, 'S', True, True))
                self.fringe_nodes.append(Node(inter, 'S', False, True))
            if inter.i == H+1:
                self.fringe_nodes.append(Node(inter, 'N', True, True))
                self.fringe_nodes.append(Node(inter, 'N', False, True))
            if inter.j == 0:
                self.fringe_nodes.append(Node(inter, 'E', True, True))
                self.fringe_nodes.append(Node(inter, 'E', False, True))
            if inter.j == L+1:
                self.fringe_nodes.append(Node(inter, 'W', True, True))
                self.fringe_nodes.append(Node(inter, 'W', False, True))
        self.interm_nodes = []
        for inter in self.interm_inters:
            for dir in ['E', 'N', 'W', 'S']:
                self.interm_nodes.append(Node(inter, dir, True, False))
                self.interm_nodes.append(Node(inter, dir, False, False))
        self.nodes = self.fringe_nodes + self.interm_nodes

    def construct_edges(self):
        H = self.H
        L = self.L
        dir_dict = Component.dir_dict
        opposite_dir = Component.opposite_dir
        turn_left_dir = Component.turn_left_dir
        turn_right_dir = Component.turn_right_dir
        self.edges = []
        for node in self.interm_nodes:
            if node.is_incoming:
                dir_tuple = dir_dict[node.dir]
                from_inter = node.inter + dir_tuple
                i = from_inter.i
                j = from_inter.j
                is_fringe = True if i == 0 or i == H+1 or j == 0 or j == L+1 else False
                from_node_idx = self.nodes.index(Node(from_inter, opposite_dir[node.dir], False, is_fringe))
                turn_left_node_idx = self.nodes.index(Node(node.inter, turn_left_dir[node.dir], False, False))
                go_straight_node_idx = self.nodes.index(Node(node.inter, opposite_dir[node.dir], False, False))
                turn_right_node_idx = self.nodes.index(Node(node.inter, turn_right_dir[node.dir], False, False))
                from_node = self.nodes[from_node_idx]
                turn_left_node = self.nodes[turn_left_node_idx]
                go_straight_node = self.nodes[go_straight_node_idx]
                turn_right_node = self.nodes[turn_right_node_idx]
                self.edges.append(Edge(from_node, node, False))
                self.edges.append(Edge(node, turn_left_node, True))
                self.edges.append(Edge(node, go_straight_node, True))
                self.edges.append(Edge(node, turn_right_node, True))
        for node in self.fringe_nodes:
            if node.is_incoming:
                dir_tuple = dir_dict[node.dir]
                from_inter = node.inter + dir_tuple
                from_node_idx = self.nodes.index(Node(from_inter, opposite_dir[node.dir], False, False))
                from_node = self.nodes[from_node_idx]
                self.edges.append(Edge(from_node, node, False))
    
    def blit(self, screen):
        for inter in self.inters:
            inter.blit(screen)
        for node in self.nodes:
            node.blit(screen)
        for edge in self.edges:
            edge.blit(screen)

# initialization test
if __name__ == '__main__':
    pygame.init()
    logo = pygame.image.load('images/logo_32x32.png')
    pygame.display.set_icon(logo)
    pygame.display.set_caption('Congestion Control Simulation')
    screen = pygame.display.set_mode((960, 960))
    graph = Graph(3, 3)
    graph.blit(screen)
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False