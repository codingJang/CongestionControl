"""
from ray.rllib.env.multi_agent_env import MultiAgentEnv
import pygame
import gym
import numpy as np


class Traffic(MultiAgentEnv):
    def __init__(self, config=None):
        config = config or {}
        self.width = config.get("width", 10)
        self.height = config.get("height", 10)

        self.timestep_limit = config.get("ts", 100)
        
        self.observation_space = 
"""