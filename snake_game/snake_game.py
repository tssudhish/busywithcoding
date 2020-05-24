# -*- coding: utf-8 -*-
import os
import pygame
import gym
import numpy as np
from random import randint
from gym import error, spaces, utils
from gym.utils import seeding
import json



with open('conf.json') as f:
    data = json.load(f)


def get_env_options(env_var, valid_list=None, default_value=None):
    try:
        env_var=os.environ[env_var]
        if valid_list:
            return valid_list[valid_list.index(env_var.lower())]
        else:
            return env_var.lower()
    except:
        print("Cannot find the input variable or the valid list")
        env_var=default_value
    return env_var

SCREEN_SIZE=get_env_options("SCREEN_SIZE",
                            valid_list=["small","large","medium"],
                            default_value="small")


class snake_game(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
      self.screen_size=tuple(data["screen_size"][SCREEN_SIZE]) # not the actual screen size . Should multiply by snake_head_size.
      self.snake_head_size,self.snake_length=tuple(data["snake_size"])
      self.observation_space= spaces.Box(np.array([0,0]),
                                          np.array(self.screen_size),
                                          dtype=np.int64)
      self.action_space = spaces.Discrete(2)
      pass

  def step(self, action):
      pass

  def reset(self):
      pass

  def render(self, mode='human', close=False):
      pass


