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
    data =json.loads(f.read())

print(data)

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



class Segment(pygame.sprite.Sprite):
    rotate_left      = np.array([[0,-1],[1,0]])
    rotate_right     = np.array([[0,1],[-1,0]])

    def __init__(self,loc,direction, type='body'):
        pygame.sprite.Sprite.__init__(self)
        self.loc=loc   # loc should be an np.array of size 2
        self.type=type
        self.size,_=tuple(data["snake_size"])     # currently 10 pixel at a time will move
        self.direction=direction
        self.render()
    
    #------------------View---------------------------------------------------
    def render(self):
        if pygame.get_init():
            self.image = pygame.Surface([self.size, self.size])
            self.image.fill(data["color"]["snake_color"])
            self.rect = self.image.get_rect()
            self.rect.x,self.rect.y=self.loc

    #------------------Model--------------------------------------------------
    def turn_head(self,action=None):
        """
            action should change direction and start moving the snake.
            action is the rotation matrix for left and right.
            
            
            i.e. snake moving right, then left will take it up, right will take
            it down.
            snake moving left, then left will take it down, right will take it
            up.
            snake moving down, then left will take it right, right will take 
            it left.
            snake moving up, left will take it left, right will take it right.
            This can be done through 2D vector algebra.
            Needs to be refined that way.
        """
        new_direction=self.direction
        if self.type == 'head':
            if action == 1:
                new_direction=self.direction.dot(self.rotate_right)
            elif action == 0:
                new_direction=self.direction.dot(self.rotate_left)
            else:
                new_direction=self.direction
        self.direction=new_direction
        
    def move(self,action=None):
        self.turn_head(action)
        self.loc+=self.speed*self.direction
        self.render()
    
    

class Snake(pygame.sprite.Group):
    def __init__(self,h_loc):
        super(pygame.sprite.Group,self).__init__()
        self.head_location=h_loc # np.array([x,y])
        self.scale,self.length=tuple(data["snake_size"])     # currently 10 pixel at a time will move
        self.direction=self.scale*np.array([0,1]) # initial snake will move to the right
        self.create_snake()

    #-----------------Model---------------------------------------------------
    def create_snake(self):
        segment_location=self.head_location
        head=Segment(segment_location,self.direction,type='head')
        self.add_segment(head)
        for body in range(self.length):
            segment_location-=self.direction
            body=Segment(segment_location,self.direction)
            self.add_segment(body)

    def move(self,action=None,screen=None):
        for body in self.sprites:
            body.move(action)
        self.render(screen)

    def add_segment(self,segment):
        self.add(segment)
    #-----------------View----------------------------------------------------
    def render(self,screen=None):
        for body in self.sprites():
            body.render()
        if pygame.get_init():
            self.draw(screen)
        

class Snake_Game(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self,mode="human"):
        self.screen_size=tuple(data["screen_size"][SCREEN_SIZE]) # not the actual screen size . Should multiply by snake_head_size.
        self.snake_head_size,self.snake_length=tuple(data["snake_size"])
        self.observation_space= spaces.Box(np.array([0,0]),
                                            np.array(self.screen_size),
                                            dtype=np.int64)
        self.action_space = spaces.Discrete(2)
        self.snake=Snake(self.observation_space.sample())
        self.dead=False
        self.mode=mode
        pass

   #----------------------------------Model ---------------------------------- 
    
    def step(self, action):
        pass
    
    def reset(self):
        pass
    
    def render(self, mode='human', close=False):
        print("default mode = {}".format(mode))
        self.create_game_view(mode)
        pass
    
   #----------------------------------View -----------------------------------
    def background(self):
        
        pass
        
    def create_game_view(self, mode):
        # use render mode
        print("Incoming mode - {}".format(mode))
        if all([not pygame.get_init(),mode in self.metadata["render.modes"]]):
            # Call this function so the Pygame library can initialize itself
            pygame.init()
            if pygame.get_init():
                pygame.display.set_caption('SNAKE GAME')
                self.screen = pygame.display.set_mode(self.screen_size)
                print("Captured screen - {}".format(self.screen))
                self.screen.fill(data["color"]["background"])
                self.snake.render(self.screen)
                pygame.event.pump()
                pygame.display.update()
            
    
def main():
    clock = pygame.time.Clock()
    move_list=[pygame.K_LEFT,
               pygame.K_RIGHT]
    
    game=Snake_Game()
    game.render()
    # while not game.dead and game.mode=="human":
    #     for e in pygame.event.get():
    #         if e.type == pygame.QUIT:
    #             game.running = 0
    #         elif e.type == pygame.KEYDOWN:
    #             try:
    #                 game.step(move_list.index(e.key))
    #             except:
    #                 print("This movement for key {} not defined".format(e.key))
    #         # elif e.type == pygame.MOUSEBUTTONDOWN:
    #         #     pos=pygame.mouse.get_pos()
    #         #     if game.score_board.isOver(pos):
    #         #         print("clicked refresh button")
    #         #         game.reset()
    
    #     # game.check_game_status()
    #     pygame.display.update()
    #     clock.tick(data["FPS"])
    # pygame.quit()
    return game

if __name__=="__main__":
    g=main()
    # pygame.quit()