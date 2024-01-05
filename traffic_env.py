
from ray.rllib.env.multi_agent_env import MultiAgentEnv
import pygame
import gym
import numpy as np


class Intersection:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __eq__(self, other):
        return (self.i == other.i) and (self.j == other.j)
    
    def __add__(self, other):
        return Intersection(self.i + other[0], self.j + other[1])

class Node:
    def __init__(self, inter, dir, is_incoming, is_fringe):
        self.inter = inter
        self.dir = dir
        self.is_incoming = is_incoming
        self.is_fringe = is_fringe

class Edge:
    delta_tL = 10  # timesteps
    delta_tI = 2   # timesteps
    def __init__(self, start_node, end_node, is_inter):
        self.start_node = start_node
        self.end_node = end_node
        self.is_inter = is_inter
        self.delta_t = Edge.delta_tI if is_inter else Edge.delta_tL

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
        self.edges = []
        for node in self.interm_nodes:
            if node.is_incoming:
                dir_vec = dir_dict[node.dir]
                coming_from_inter = 
                




            


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