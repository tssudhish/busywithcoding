# -*- coding: utf-8 -*-
import os
import pygame
import gym
import numpy as np
from random import randint
from gym import error, spaces, utils
from gym.utils import seeding
import json



"""
Following lessons in https://alexandervandekleut.github.io/
to get the concept correct.

"""






























with open('conf.json') as f:
    data =json.loads(f.read())

# #print(data)

# def get_env_options(env_var, valid_list=None, default_value=None):
#     try:
#         env_var=os.environ[env_var]
#         if valid_list:
#             return valid_list[valid_list.index(env_var.lower())]
#         else:
#             return env_var.lower()
#     except:
# #        print("Cannot find the input variable or the valid list")
#         env_var=default_value
#     return env_var

# SCREEN_SIZE=get_env_options("SCREEN_SIZE",
#                             valid_list=["small","large","medium"],
#                             default_value="small")



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
    def render(self,screen):
        self.fill(data["color"]["red"])
        self.rect=self.get_rect()
        screen.blit(self,self.location)
           
class Snake(pygame.sprite.Group):
    location_list=[]
    rotate_left      = np.array([[0,-1],[1,0]])
    rotate_right     = np.array([[0,1],[-1,0]])
   
    def __init__(self,h_loc,direction,num_segment):
        """
        a Snake class which has all attributes and methods describing a snake.
        1. Size of the snake - number of segments/length of segments
        2. location of each of the segments
        3. move one step in a given direction
            a. head moves in a specific direction
            b. rest of the bodies just start occupying the spaces of previous body
        4. grow in size.
            a. growth happens at the head. by creating a segment located at the same
               place as that of the head. then when the head has moved forward it appears.
        5. head can crash into other sprites and bodies and should be checked.
        """
        super(pygame.sprite.Group,self).__init__()
#        print(f"Head Location {h_loc}")
#        print(f"Direction {direction}")
        self.head_location=np.array(h_loc) # np.array([x,y])
        self.direction=np.array(direction) # initial snake will move to the right
        self.location_list=[np.array([0,0])]*num_segment
        self.initialize_location_list()
        self.initialize_snake_segments()
       
    def initialize_location_list(self):
        self.location_list[0]=self.head_location
        location_segment=self.head_location
        for i in range(1,len(self.location_list)):
            location_segment=np.subtract(location_segment,self.direction)
            self.location_list[i]=location_segment
    
    def turn_head(self,left=True):
        if left:
            rotate_direction = self.rotate_left
        else:
            rotate_direction=self.rotate_right
        
        self.direction=self.direction.dot(rotate_direction)

    def move_head_forward(self):
        self.location_list[0]=np.add(self.location_list[0],self.direction)
        
        
    def inch(self):
        loc_list=self.location_list.copy()
        num_segment=len(loc_list)
        # print(f"num_segment = {num_segment}")
        self.move_head_forward()
        for i in range(1,num_segment):
            # print(f"location: {i}")
            self.location_list[i]=loc_list[i-1]
        self.head_location=self.location_list[0]
        # print(f"location list: {self.location_list}")
        return self.update_view()
        
    def update_view(self):
        for seg,seg_loc in zip(self.sprites(),self.location_list):
            seg.update_location(seg_loc)
        if self.crash_with_self():
            print("Crashed")
            return True

        
    def grow(self):
        segment_index=1
        self.location_list.insert(segment_index,self.location_list[0]) # add a segment at the location same as the head
        self.move_head_forward()
        self.add_segment(segment_index)
        return self.update_view()
        pass
    
    def crash_with_self(self):
        crashed = pygame.sprite.spritecollideany(self.sprites()[0], self.sprites()[1:])
        if crashed:
            return True
    
    def add_segment(self,segment_index):
        s=Segment(self.location_list[segment_index])
        # if segment_index==0:
        #     s.seg_type="head"
        s.setimage()
        self.add(s)
        pass

    def initialize_snake_segments(self):
        for i in range(len(self.location_list)):
            self.add_segment(i)
        return self.update_view()
    
    def render(self,screen):
        self.draw(screen)
            
class Snake_Game(gym.Env):
    metadata = {'render.modes': ['human']}
    scaling_factor   = 10 # Scaling
    
    def __init__(self,mode="human",size="small"):
        pygame.init()
        pygame.display.set_caption('SNAKE GAME')
        self.screen_size=tuple(data["screen_size"][size])
        self.screen= pygame.display.set_mode(self.screen_size)
        self.screen.fill(data["color"]["background"])
        pygame.display.update()
        self.clock=pygame.time.Clock()
        self.observation_space= spaces.Box(np.array([0,0]),
                                            np.array([int(v/self.scaling_factor)
                                            for v in self.screen_size]),
                                            dtype=np.int64)
        self.action_space = spaces.Discrete(2)
        self.dead=False
        self.mode=mode
        
        pass
    
    def add_snake(self):
        # start a snake at a location at least 5 units away from 
        # snake_seed=tuple(self.scaling_factor*np.random.randint(5,
        #                                                  self.observation_space.high[0],
        #                                                  size=2,
        #                                                  dtype='int'))
        snake_seed=(50,50)
        snake_direction=tuple(self.scaling_factor*np.array([1,0]))# snake is horizontal
        self.snake=Snake(snake_seed,snake_direction,5)
        
    def loop_snake(self):
        # print(self.snake.head_location)
        pass
    def add_food(self):
        self.food_location=self.scaling_factor*self.observation_space.sample() # 10 is the scaling factor
        self.food=Food(self.food_location)

    def snake_eat_food(self):
        if self.snake.grow():
            self.dead=True
        self.add_food()
        pass

    def clear_screen(self):
        self.screen.fill(data["color"]["background"])


    def move(self):
        if self.snake_can_eat_food():             # Check if food is there to be eaten
            self.snake_eat_food()
        check_crash=self.snake.inch()             # move forward
        self.loop_snake()
        print(f"check crash: {check_crash}")
        if check_crash:
            print("crashed at move")
            self.dead=True

    def quit(self):
        pygame.quit()
        
    def render(self):
        self.clear_screen()                 # clear the game screen
        self.food.render(self.screen)       # show the food in the screen
        self.snake.render(self.screen)      # draw the snake on the screen.
        pygame.display.update()             # update the display of the game.
        pass
        
    
    def snake_can_eat_food(self):
        # print(f"head location = {self.snake.head_location}")
        # print(f"head direction = {self.snake.direction}")
        # print(f"food location = {self.food.location}")
        head_step_location=self.snake.head_location+self.snake.direction
        if (head_step_location==self.food_location).all():
            return True
        else:
            return False
    def step(self,index):
        # print(f"Incoming index: {index}")
        self.snake.turn_head(index)

    



def main():
    clock = pygame.time.Clock()
    move_list=[pygame.K_RIGHT,
               pygame.K_LEFT]
    pygame.init()
    game=Snake_Game()
    game.clear_screen()
    game.add_food()
    game.add_snake()
    game.render()
    # game.dead=False
    game.mode="human"
    while not game.dead and game.mode=="human":
        for e in pygame.event.get():
            # print(f"event: {e}")
            if e.type == pygame.QUIT:
                game.dead = True
            elif e.type == pygame.KEYDOWN:
                try:
                    game.step(move_list.index(e.key))
                except:
                    print("This movement for key {} not defined".format(e.key))
        game.move()
        game.render()
        pygame.display.update()
        clock.tick(data["FPS"])
    pygame.quit()
    return game

if __name__=="__main__":
    g=main()
    # pygame.quit()
