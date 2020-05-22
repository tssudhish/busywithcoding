# -*- coding: utf-8 -*-
"""
Created on Mon May 18 14:07:18 2020

@author: Sudhish Kumar
"""

from gym  import Env

class Game_Env(Env):
    """Base class derived from gym Env to be used by actual game for tensorflow"""
    def __init__(self):
        super(Env,self).__init__()

