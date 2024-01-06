
from ray.rllib.env.multi_agent_env import MultiAgentEnv
import pygame
from pygame.sprite import Sprite, Group
import gym
import numpy as np


class Intersection(Sprite):
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j
    
    def __add__(self, other):
        return Intersection(self.i + other[0], self.j + other[1])


class Node(Sprite):
    def __init__(self, inter, dir, is_incoming, is_fringe):
        self.inter = inter
        self.dir = dir
        self.is_incoming = is_incoming
        self.is_fringe = is_fringe
    
    def __eq__(self, other):
        is_eq = True
        for self_var, other_var in zip(vars(self), vars(other)):
            is_eq = is_eq and (self_var == other_var)
        return is_eq


class Edge(Sprite):
    delta_tL = 10  # timesteps
    delta_tI = 2   # timesteps
    def __init__(self, start_node, end_node, is_inter):
        self.start_node = start_node
        self.end_node = end_node
        self.is_inter = is_inter
        self.delta_t = Edge.delta_tI if is_inter else Edge.delta_tL
        if start_node.inter == end_node.inter and not is_inter:
            raise AssertionError("Edge connects nodes internally but is_inter is False.")
        if start_node.inter == end_node.inter and not is_inter:
            raise AssertionError("Edge connects nodes from different intersections but is_inter is True.")
    
    def __eq__(self, other):
        return self.start_node == other.start_node and self.end_node == other.end_node


class Graph:
    def __init__(self, H, L):
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
        dir_dict = {'E':(0,1), 'N':(-1,0), 'W':(0,-1), 'S':(1,0)}
        opposite_dir = {'E':'W', 'N':'S', 'W':'E', 'S':'N'}
        turn_left_dir = {'E':'S', 'N':'E', 'W':'N', 'S':'W'}
        turn_right_dir = {'E':'N', 'N':'W', 'W':'S', 'S':'E'}

        self.edges = []
        for node in self.interm_nodes:
            if node.is_incoming:
                dir_vec = dir_dict[node.dir]
                from_inter = node.inter + dir_vec
                i = from_inter.i
                j = from_inter.j
                is_fringe = True if i == 0 or i == H+1 or j == 0 or j == L+1 else False
                from_node_idx = self.nodes.index(Node(from_inter, opposite_dir[node.dir], False, is_fringe))
                turn_left_node_idx = self.nodes.index(Node(node.inter, turn_left_dir[self.dir], False, False))
                go_straight_node_idx = self.nodes.index(Node(node.inter, opposite_dir[self.dir], False, False))
                turn_right_node_idx = self.nodes.index(Node(node.inter, turn_right_dir[self.dir], False, False))
                from_node = self.nodes[from_node_idx]
                turn_left_node = self.nodes[turn_left_node_idx]
                go_straight_node = self.nodes[go_straight_node_idx]
                turn_right_node = self.nodes[turn_right_node_idx]
                self.edges.append(Edge(from_node, node))
                self.edges.append(Edge(node, turn_left_node))
                self.edges.append(Edge(node, go_straight_node))
                self.edges.append(Edge(node, turn_right_node))
        for node in self.fringe_nodes:
            if node.is_incoming:
                dir_vec = dir_dict[node.dir]
                from_inter = node.inter + dir_vec
                from_node_idx = self.nodes.index(Node(from_inter, opposite_dir[node.dir], False, False))
                from_node = self.nodes[from_node_idx]
                self.edges.append(Edge(from_node, node))

if __name__ == '__main__':
    pygame.init()
    logo = pygame.image.load('logo_32x32.png')
    pygame.display.set_icon(logo)
    pygame.display.set_caption('Congestion Control Simulation')
    screen = pygame.display.set_mode((720, 720))
    graph = Graph(3, 3)
    graph.draw(screen)
    running = True
    while running:
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
    
    graph.blit()

"""
class Car:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def nearest_intermediate_node(self, fringe_node):
        # calculate nearest_intermediate_node
        pass
    def create_path(self):
        start_interm = self.nearest_intermediate_node(self.start).coord
        end_interm = self.nearest_intermediate_node(self.end).coord

class Traffic(MultiAgentEnv):
    def __init__(self, config=None):
        config = config or {}
        self.width = config.get("width", 10)
        self.height = config.get("height", 10)

        self.timestep_limit = config.get("ts", 100)
        
        self.observation_space = 
"""