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

#print(data)

def get_env_options(env_var, valid_list=None, default_value=None):
    try:
        env_var=os.environ[env_var]
        if valid_list:
            return valid_list[valid_list.index(env_var.lower())]
        else:
            return env_var.lower()
    except:
#        print("Cannot find the input variable or the valid list")
        env_var=default_value
    return env_var

SCREEN_SIZE=get_env_options("SCREEN_SIZE",
                            valid_list=["small","large","medium"],
                            default_value="small")



class Segment(pygame.sprite.Sprite):

    def __init__(self,loc,segment_type='body'):
        super().__init__()
        self.seg_type=segment_type
        self.name="default_segment"
        self.loc=loc
    

    #------------------View---------------------------------------------------
    def setimage(self):
        if pygame.get_init():
            self.size,_=tuple(data["snake_size"])     # currently 10 pixel at a time will move
            self.image = pygame.Surface([self.size, self.size])
#            self.image.fill(data["color"]["snake_color"])
            self.image.fill(data["color"]["background"])
            self.get_snake_image(self.size-2,self.size-2)
            self.image.blit(self.image_top,(1,1))
            self.rect = self.image.get_rect()
            
    def get_snake_image(self,w,h):
        if self.seg_type=="head":
            background = pygame.image.load('images/snake_head_right.bmp')#.convert_alpha()
        else:
            background = pygame.image.load('images/snake_body.bmp')#.convert_alpha()
        background = pygame.transform.rotate(background,0)
        background = pygame.transform.scale(background, (w,h))
        self.image_top=background
            
    def update_location(self, loc):
        self.loc=loc
        if self.rect:
            self.rect.x,self.rect.y=self.loc
    

class Food(pygame.surface.Surface):
    value=1
    def __init__(self,location):
        self.size,_=tuple(data["snake_size"])   # food is same size as snake head
        self.location=location                  # location of food in tuple
        print(type(self.size))
        super().__init__((self.size,self.size))
        
        


            
#        print("Created snake segment at location {}".format(self.loc))
#        self.rect.x,self.rect.y=self.loc

    #------------------Model--------------------------------------------------
#    def turn_head(self,action=None):
#        """
#            action should change direction and start moving the snake.
#            action is the rotation matrix for left and right.
#            
#            
#            i.e. snake moving right, then left will take it up, right will take
#            it down.
#            snake moving left, then left will take it down, right will take it
#            up.
#            snake moving down, then left will take it right, right will take 
#            it left.
#            snake moving up, left will take it left, right will take it right.
#            This can be done through 2D vector algebra.
#            Needs to be refined that way.
#        """
#        new_direction=self.direction
#        if self.type == 'head':
#            if action == 1:
#                new_direction=self.direction.dot(self.rotate_right)
#            elif action == 0:
#                new_direction=self.direction.dot(self.rotate_left)
#            else:
#                new_direction=self.direction
#        self.direction=new_direction
        
#    def move(self,action=None):
#        self.turn_head(action)
#        self.loc+=self.speed*self.direction
#        self.render()
    
#    
#
class Snake(pygame.sprite.Group):
    location_list=[]
    
    def __init__(self,h_loc,direction,num_segment):
        super(pygame.sprite.Group,self).__init__()
        self.head_location=h_loc # np.array([x,y])
        self.direction=direction # initial snake will move to the right
        self.num_segment=num_segment
        self.initialize_location_list()
        self.initialize_snake_segments()
        

    def initialize_location_list(self):
        self.location_list.append(self.head_location)
        location_segment=self.head_location
        for i in range( self.num_segment):
            location_segment=np.subtract(location_segment,self.direction)
            self.location_list.append(location_segment)

    def inch(self):
        loc_list=self.location_list.copy()
        self.location_list[0]=np.add(self.location_list[0],self.direction)
        for i in range(1,self.num_segment+1):
            self.location_list[i]=loc_list[i-1]
    
    def update_view(self):
        for seg,seg_loc in zip(self.sprites(),self.location_list):
            seg.update_location(seg_loc)

    def initialize_snake_segments(self):
        for i,seg_loc in enumerate(self.location_list):
            s=Segment((0,0))
            if i==0:
                s.seg_type="head"
            s.setimage()
            s.update_location(seg_loc)
            self.add(s)
        
    
    #-----------------Model---------------------------------------------------
#    def create_snake(self):
#        segment_location=self.head_location
#        head=Segment(segment_location,self.direction,type='head')
#        print("segment_location - {}".format(segment_location))
#        self.add_segment(head)
#        for body in range(self.length):
#            segment_location-=self.direction
#            print("segment_location - {}".format(segment_location))
#            body=Segment(segment_location,self.direction)
#            print("body.location - {}".format(body.loc))
#            self.add_segment(body)
#        
##
#    def move(self,action=None,screen=None):
#        for body in self.sprites():
#            body.move(action)
#        self.render(screen)
#
#    def add_segment(self,segment):
#        self.add(segment)
#    #-----------------View----------------------------------------------------
#    def render(self,screen=None):
#        print("screen at Snake - {}".format(screen))
#        for body in self.sprites():
#            print("Name-{} location-{}".format(body.name,body.loc))
#            body.render(screen)
#        if pygame.get_init():
#            self.draw(screen)
##        
#
class Snake_Game(gym.Env):
    metadata = {'render.modes': ['human']}
    rotate_left      = np.array([[0,-1],[1,0]])
    rotate_right     = np.array([[0,1],[-1,0]])
    

    def __init__(self,mode="human",size="small"):
        pygame.init()
        pygame.display.set_caption('SNAKE GAME')
        self.screen_size=tuple(data["screen_size"][size])
        self.screen= pygame.display.set_mode(self.screen_size)
        self.screen.fill(data["color"]["background"])
        pygame.display.update()
        self.clock=pygame.time.Clock()
        self.observation_space= spaces.Box(np.array([0,0]),
                                            np.array(self.screen_size),
                                            dtype=np.int64)
        self.action_space = spaces.Discrete(2)
        self.dead=False
        self.mode=mode
        pass

    def clear_screen(self):
        self.screen.fill(data["color"]["background"])

    def move(self):
        self.clear_screen()
        self.snake.draw() # snake object should be created befor running this
        pygame.display.update()



    def quit(self):
        pygame.quit()
#   #----------------------------------Model ---------------------------------- 
#    
#    def step(self, action):
#        pass
#    
#    def reset(self):
#        pass
#    
#    def render(self, mode='human', close=False):
#        print("default mode = {}".format(mode))
#        self.create_game_view(mode)
#        pass
#    
#   #----------------------------------View -----------------------------------
#    def background(self):
#        
#        pass
#        
#    def create_game_view(self, mode):
#        # use render mode
#        print("Incoming mode - {}".format(mode))
#        if mode == "human":
#            # Call this function so the Pygame library can initialize itself
#            pygame.init()
#            if pygame.get_init():
#                pygame.display.set_caption('SNAKE GAME')
#                self.screen = pygame.display.set_mode(self.screen_size)
#                print("Captured screen - {}".format(self.screen))
#                self.screen.fill(data["color"]["background"])
#                self.snake.render(self.screen)
#                pygame.event.pump()
#                pygame.display.update()
#            
#    
    
def clear_screen(screen):
    screen.fill(data["color"]["background"])
    
def update_snake(new_loc,screen):
    snake.sprites()[0].update_location(new_loc)
    snake.draw(screen)    
    pygame.display.update()

def move(screen):
    clear_screen(screen)
    snake.draw(screen)
    pygame.display.update()
    

    
pygame.init()
pygame.display.set_caption('SNAKE GAME')
screen= pygame.display.set_mode((320,300))
screen.fill(data["color"]["background"])
pygame.display.update()
clock=pygame.time.Clock()


f=Food()
f.fill(data["color"]["red"])
f.rect=f.get_rect()
print(100,100)
screen.blit(f,(100,100))
pygame.display.update()

clock.tick(1)

print(50,50)

clear_screen(screen)
screen.blit(f,(50,50))
pygame.display.update()
clock.tick(5)



snake=pygame.sprite.Group()

location_list=[]
head_location=np.array([100,100])
direction=np.array([10,0])


snake=Snake(head_location,direction,10)
move(screen)
direction=np.array([0,-10])
snake.direction=direction
clock=pygame.time.Clock()
for i in range(10):
    pygame.event.pump()
    snake.inch()
    snake.update_view()
    move(screen)
    clock.tick(5)



    
    








#def main():
#    clock = pygame.time.Clock()
#    move_list=[pygame.K_LEFT,
#               pygame.K_RIGHT]
#    pygame.init()
#    game=Snake_Game()
#    game.render()
#    pygame.quit()
##    game.render()
#    # while not game.dead and game.mode=="human":
#    #     for e in pygame.event.get():
#    #         if e.type == pygame.QUIT:
#    #             game.running = 0
#    #         elif e.type == pygame.KEYDOWN:
#    #             try:
#    #                 game.step(move_list.index(e.key))
#    #             except:
#    #                 print("This movement for key {} not defined".format(e.key))
#    #         # elif e.type == pygame.MOUSEBUTTONDOWN:
#    #         #     pos=pygame.mouse.get_pos()
#    #         #     if game.score_board.isOver(pos):
#    #         #         print("clicked refresh button")
#    #         #         game.reset()
#    
#    #     # game.check_game_status()
#    #     pygame.display.update()
#    #     clock.tick(data["FPS"])
#    # pygame.quit()
#    return game
#
#if __name__=="__main__":
#    g=main()
#    # pygame.quit()
