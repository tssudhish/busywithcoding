#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 13:03:29 2020

@author: pi
"""
import pygame
import os
class Score(pygame.surface.Surface):
    
    def __init__(self,h,w):
        super().__init__( (h,w))
        self.height = h
        self.width = w
        self.fill((155, 111, 111))
        if not pygame.font.get_init():
            pygame.font.init()
        self.arial_font = pygame.font.SysFont('Arial', 16)
        pass
    