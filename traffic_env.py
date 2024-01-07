
from ray.rllib.env.multi_agent_env import MultiAgentEnv
import pygame
import gym
import numpy as np

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