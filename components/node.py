import pygame
from pygame.math import Vector2
from collections import deque
from components.component import Component
from components.intersection import Intersection
from components.methods.methods import center_blit, center_rect, to_vector2


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
        if is_incoming and not is_fringe:
            self.lt_queue = deque()
            self.gs_queue = deque()
            self.lt_signal = False
            self.rt_signal = False
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
            node_loc += 0.08 * to_vector2(tup_dir_dict[rt_dir_dict[self.dir]])
        else:
            node_loc += 0.08 * to_vector2(tup_dir_dict[lt_dir_dict[self.dir]])
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
                gs_edge.end_node.gs_edge = gs_edge
            if rt_edge is not None:
                assert self is rt_edge.start_node, "rt_edge's start_node should be oneself."
                self.rt_edge = rt_edge
                rt_edge.end_node.rt_edge = rt_edge
    
    def blit(self, screen):
        pygame.draw.circle(screen, self.color, self.loc, 5, 0)
    
    def step(self, screen=None):
        if self.is_incoming and not self.is_fringe:
            for _ in range(self.v_star):
                inter = self.inter
                if self.lt_queue and inter.traffic_light[inter.mode, inter.idx_1[self.dir], inter.idx_2['lt']]:
                    lt_vehicle = self.lt_queue.pop()
                    lt_vehicle.current = self.lt_edge
                    lt_vehicle.current_idx += 1
                    lt_vehicle.timer = 0
                if self.gs_queue and inter.traffic_light[inter.mode, inter.idx_1[self.dir], inter.idx_2['gs']]:
                    gs_vehicle = self.gs_queue.pop()
                    gs_vehicle.current = self.gs_edge
                    gs_vehicle.current_idx += 1
                    gs_vehicle.timer = 0
        if screen is not None:
            self.blit(screen)
        self.time += 1