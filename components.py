import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2
from collections import deque
from methods import *

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

    def blit(self, screen=None):
        pass
    
    def step(self, action, screen=None):
        self.t += 1
        if screen is not None:
            self.blit(screen)


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
        
    def blit(self, screen=None):
        center_blit(self, screen)

    def step(self, action, screen=None):
        if action is None:
            action = (self.t % 16) // 2
        else:
            self.action = action
        self.blit(screen)
        super(Intersection, self).step(screen=screen)


class Node(Component):
    """
    Node at a given intersection oriented in some direction,
    with bool values for is_incoming and is_fringe.
    """
    def __init__(self, inter, dir, is_incoming, is_fringe, v_star=2, time=0):
        super(Node, self).__init__(time=time)
        self.inter = inter
        self.dir = dir
        self.is_incoming = is_incoming
        self.is_fringe = is_fringe
        if is_incoming:
            self.lt_queue = deque()
            self.gs_queue = deque()
        self.v_star = v_star
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
        return f"i={self.inter.i}, j={self.inter.j}, dir={self.dir}, \
is_incoming={self.is_incoming}, is_fringe={self.is_fringe}"

    def set_color(self):
        color_value = (255, 0, 0) if self.is_incoming else (0, 0, 255)
        self.color = pygame.color.Color(*color_value)
    
    def set_location(self):
        node_loc = Vector2(self.inter.loc)
        tup_dir_dict = Component.tup_dir_dict
        lt_dir_dict = Component.lt_dir_dict
        rt_dir_dict = Component.rt_dir_dict
        node_loc += 0.20 * to_vector2(tup_dir_dict[self.dir])
        if self.is_incoming:
            node_loc += 0.08 * to_vector2(tup_dir_dict[lt_dir_dict[self.dir]])
        else:
            node_loc += 0.08 * to_vector2(tup_dir_dict[rt_dir_dict[self.dir]])
        self.loc = node_loc
    
    def connect_to_edge(self, from_edge=None, lt_edge=None, gs_edge=None, rt_edge=None):
        if from_edge is not None:
            assert self is from_edge.end_node, "from_edge's end_node should be oneself."
            self.from_edge = from_edge
            from_edge.start_node.to_edge = from_edge
        if not self.is_fringe:
            if lt_edge is not None:
                assert self is lt_edge.start_node, "lt_edge's start_node should be oneself."
                self.lt_edge = lt_edge
                lt_edge.end_node.lt_edge = lt_edge
            if gs_edge is not None:
                assert self is gs_edge.start_node, "gs_edge's start_node should be oneself."
                self.gs_edge = gs_edge
                gs_edge.end_node.lt_edge = gs_edge
            if rt_edge is not None:
                assert self is rt_edge.start_node, "rt_edge's start_node should be oneself."
                self.rt_edge = rt_edge
                rt_edge.end_node.lt_edge = rt_edge
    
    def blit(self, screen):
        pygame.draw.circle(screen, self.color, self.loc, 5, 0)
    
    def update(self, screen=None):
        if self.is_incoming:
            for i in range(self.v_star):
                vehicle = self.lt_queue.pop()
                
        super(Intersection, self).update(screen=screen)


class Edge(Component):
    delta_tL = 10  # timesteps
    delta_tI = 2   # timesteps
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


class Graph(Component):
    def __init__(self, H, L, time=0):
        super(Graph, self).__init__(time=time)
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
        tup_dir_dict = Component.tup_dir_dict
        op_dir_dict = Component.op_dir_dict
        lt_dir_dict = Component.lt_dir_dict
        rt_dir_dict = Component.rt_dir_dict
        self.edges = []
        for node in self.interm_nodes:
            if node.is_incoming:
                dir_tuple = tup_dir_dict[node.dir]
                from_inter = node.inter + dir_tuple
                i = from_inter.i
                j = from_inter.j
                is_fringe = True if i == 0 or i == H+1 or j == 0 or j == L+1 else False
                from_node_idx = self.nodes.index(Node(from_inter, op_dir_dict[node.dir], False, is_fringe))
                lt_node_idx = self.nodes.index(Node(node.inter, lt_dir_dict[node.dir], False, False))
                gs_node_idx = self.nodes.index(Node(node.inter, op_dir_dict[node.dir], False, False))
                rt_node_idx = self.nodes.index(Node(node.inter, rt_dir_dict[node.dir], False, False))
                from_node = self.nodes[from_node_idx]
                tl_node = self.nodes[lt_node_idx]
                gs_node = self.nodes[gs_node_idx]
                rt_node = self.nodes[rt_node_idx]
                from_edge = Edge(from_node, node, False)
                tl_edge = Edge(node, tl_node, True)
                gs_edge = Edge(node, gs_node, True)
                rt_edge = Edge(node, rt_node, True)
                self.edges.append(from_edge)
                self.edges.append(tl_edge)
                self.edges.append(gs_edge)
                self.edges.append(rt_edge)
                node.connect_to_edge(from_edge, tl_edge, gs_edge, rt_edge)

        for node in self.fringe_nodes:
            if node.is_incoming:
                dir_tuple = tup_dir_dict[node.dir]
                from_inter = node.inter + dir_tuple
                from_node_idx = self.nodes.index(Node(from_inter, op_dir_dict[node.dir], False, False))
                from_node = self.nodes[from_node_idx]
                from_edge = Edge(from_node, node, False)
                self.edges.append(from_edge)
                node.connect_to_edge(from_edge)
    
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