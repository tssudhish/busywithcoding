# %load game_2048.py
import os
import pygame
from random import randrange
import numpy as np
import logging
from debug import timethis, logged

#import ConfigParser

#Constants
#CONFIG = ConfigParser.ConfigParser()
#CONFIG.readfp(open('game.conf'))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255,0,0)
BACKGROUND= (251, 248, 239)
BOXBACKGROUND=(177, 181, 180)
FPS   = 150
SCREEN_WIDTH=400
SCREEN_HEIGHT=600
BOX_WIDTH=360
BOX_HEIGHT=BOX_WIDTH
#GAME_MODE="live"
GAME_MODE="debug"
#GAME_MODE="training"

BOX_ORIGIN_x=(SCREEN_WIDTH-BOX_WIDTH)/2
BOX_ORIGIN_y=(SCREEN_HEIGHT-SCREEN_WIDTH)+BOX_ORIGIN_x


NUMBER_OF_TILE=4 #4X4

TILE_GAP=5
TILE_SIZE=(BOX_WIDTH-(TILE_GAP*(NUMBER_OF_TILE+1)))/NUMBER_OF_TILE


move=TILE_GAP/2
x_change=0
y_change=0


COLOR_DICT={ "0":(201, 189, 177),
            "2":(238, 228, 218),
            "4":(236,224,200),
            "8":(242,177,121),
            "16":(245,149,99),
            "32":(245,124,95),
            "64":(246, 93, 58),
            "128":(240,198,95),
            "256":(237, 204, 97),
            "512":(239, 160, 74),
            "1024":(237, 197, 63),
            "2048":(238, 194, 46)}


class TILE(pygame.sprite.Sprite):
    move_this_tile=False
    tile_w=TILE_SIZE
    tile_h=tile_w
    value=512
    row=0
    col=0
    fontSize=30
    
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self,r,c,v):
        self.row=r
        self.col=c
        self.value=v
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface([self.tile_w, self.tile_h])
        self.update_value()
        self.rect = self.image.get_rect()
        self.rect.x=BOX_ORIGIN_x+TILE_GAP+self.col*(TILE_SIZE+TILE_GAP)
        self.rect.y=BOX_ORIGIN_y+TILE_GAP+self.row*(TILE_SIZE+TILE_GAP)
        
    def update_value(self):
        self.get_value()
        self.image.fill(self.color)
        self.image.blit(self.valueImage,((self.tile_w-self.valueImage.get_width())/2,(self.tile_h-self.fontSize)/2))
        
    
    def get_value(self):
        self.color=COLOR_DICT[str(self.value)]
        if not pygame.font.get_init():
            pygame.font.init()
        
        value_font= pygame.font.SysFont('freesans', self.fontSize)
        if self.value==0:
            value_text=""
        else:
            value_text=  "{:^}".format(self.value)        
        self.valueImage=value_font.render(value_text, False, (139,0,0))
        
    
    
class GAME_BOX(pygame.surface.Surface):
    box_w=BOX_WIDTH
    box_h=BOX_HEIGHT
    box_loc_x=BOX_ORIGIN_x
    box_loc_y=BOX_ORIGIN_y
    color=BOXBACKGROUND
    banner="GAME OVER!"
    
    def __init__(self,display_surface):
        print("Created {} of w:{} X h:{}".format(self.__class__.__name__,self.box_w,self.box_h))
        self.display_surface=display_surface
        super().__init__([self.box_w,self.box_h],pygame.SRCALPHA)
        self.fill(self.color)
        self.rect=self.get_rect()
        self.rect.x=self.box_loc_x
        self.rect.y=self.box_loc_y
    def show(self):
        self.display_surface.blit(self,(self.rect.x,self.rect.y))
        pygame.display.update()
    def game_over(self):
        self.fill(BOXBACKGROUND+(128,))
        if not pygame.font.get_init():
            pygame.font.init()
        
        game_font= pygame.font.SysFont('freesans', 50)
        game_text=  "{:^}".format(self.banner)        
        self.Image=game_font.render(game_text, False, BLACK)
        self.blit(self.Image,(self.rect.x+TILE_GAP,
                              BOX_HEIGHT/2))
        
        self.display_surface.blit(self,(self.rect.x,self.rect.y))
        pygame.display.update()
        


class SCORE_BOARD(GAME_BOX):
    def __init__(self,display_surface):
        self.color=BOXBACKGROUND
        self.box_h=(SCREEN_HEIGHT-BOX_HEIGHT)/4
        self.box_w=self.box_w
        self.box_loc_y=(SCREEN_HEIGHT-BOX_HEIGHT)/4
        self.score=0
        self.set_fonts()
        self.loc_x=self.loc_y=0
        self.loc_width=self.loc_height=0
        self.run_number=1
        super().__init__(display_surface)
    def set_fonts(self):
        if not pygame.font.get_init():
            pygame.font.init()
        self.score_font= pygame.font.SysFont('freesans', 60)
        self.icon_font= pygame.font.SysFont('freesans', 20)
        self.small_font= pygame.font.SysFont('freesans', 15)
        
    
    def get_score(self):
        score_text=  "{}".format(self.score).rjust(5)        
        self.scoreImage=self.score_font.render(score_text, False, BLACK)
    def refresh_icon(self):
        icon_box_x=150; icon_box_y=60
        self.icon_box_loc_x=self.rect.x+200
        self.icon_box_loc_y=self.rect.y
        self.icon_box=pygame.surface.Surface((icon_box_x,icon_box_y))
        self.icon_box=self.icon_box.convert()
        self.icon_box.fill(BOXBACKGROUND)
        refreshImage = pygame.image.load(os.path.abspath("./images/icons8-refresh-40.png"))
        icon_x=100; icon_y=10
        self.icon_box.blit(refreshImage,(icon_x,icon_y))
        refreshImageRect=refreshImage.get_rect()
        self.loc_x=self.icon_box_loc_x+icon_x
        self.loc_y=self.icon_box_loc_y+icon_y
        self.loc_width=self.loc_x+refreshImageRect.width
        self.loc_height=self.loc_y+refreshImageRect.height
        text=  "{:^}".format("Restart?")        
        refreshText=self.icon_font.render(text, False, WHITE)
        self.icon_box.blit(refreshText,(10,10))
        text=  "Episode  {:04d}".format(self.run_number)        
        refreshText=self.small_font.render(text, False, RED)
        self.icon_box.blit(refreshText,(10,30))
    
    def update_score(self):
        self.get_score()
        self.refresh_icon()
        self.display_surface.blit(self,(self.rect.x,self.rect.y))     # wipe clean with rectangle
        self.display_surface.blit(self.scoreImage,(self.rect.x,self.rect.y)) # insert score
        self.display_surface.blit(self.icon_box,(self.icon_box_loc_x,self.icon_box_loc_y)) # insert refresh_icon
        pygame.display.update()

    def isOver(self, pos):
        print("incoming mouse pos: {}".format(pos))
        print("range to be checked over:({},{} -{},{})".format(self.loc_x,self.loc_y,self.loc_width,self.loc_height))
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.loc_x and pos[0] < self.loc_width:
            if pos[1] > self.loc_y and pos[1] < self.loc_height:
                return True
        return False
        


class TILES(pygame.sprite.Group):
    number_of_tiles=NUMBER_OF_TILE
    
    def __init__(self):
        super(pygame.sprite.Group,self).__init__()
        self.create_tile_array()
        
    def create_tile_array(self):
        loc = [ [ None for y in range( 4 ) ] 
             for x in range( 4 ) ]
        for r in range(NUMBER_OF_TILE):
            y=BOX_ORIGIN_y+TILE_GAP+r*(TILE_SIZE+TILE_GAP)
            for c in range(NUMBER_OF_TILE):
                x=BOX_ORIGIN_x+TILE_GAP+c*(TILE_SIZE+TILE_GAP)
                loc[r][c]=(x,y)
        self.tile_origins=loc

    def add(self, row,col,value):
        tile=TILE(row,col,value)
        super(pygame.sprite.Group,self).add(tile)


#=========================Main Game========================================
class Game_2048():
    """
    Game class for 2048
    """

    @timethis
    @logged(logging.DEBUG)
    def __init__(self):
        # Create an SCREEN_WIDTH X SCREEN_HEIGHT sized screen
        print("Initialized {}()".format(self.__class__.__name__))
        self.number_of_tiles=NUMBER_OF_TILE
        self.running=True
        self.score=0
        print("GAME_MODE - {}".format(GAME_MODE))
        if all([not pygame.get_init(),GAME_MODE=="live"]):
            # Call this function so the Pygame library can initialize itself
            pygame.init()
            if pygame.get_init():
                pygame.display.set_caption('2048')
                self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
                self.screen.fill(BACKGROUND)
                self.game_box=GAME_BOX(self.screen)
                self.game_box.show()
                self.score_board=SCORE_BOARD(self.screen)
                self.tile_group=TILES()
            else:
                print("Error!! - Unable to initialize pygame")
                raise EnvironmentError

        self.reset()
    
    def roll_left(self,arr):
        """
        Moves any given array to the left.
        The game_state is manipulated by feeding an appropriately transformed form.

        Parameters
        ----------
        arr : TYPE
            DESCRIPTION.

        Returns
        -------
        arr : TYPE
            DESCRIPTION.

        """
        row=0
        while row<np.size(arr,0):
            col=0
            while col<np.size(arr,1)-1:
                
                if not np.any(arr[row,:]):
                    break                
                elif all([arr[row,col]==0, 
                          arr[row,col+1]>0]):
                    arr[row,col]=arr[row,col+1]
                    arr[row,col+1]=0
                    self.roll_left(arr)
                elif all([arr[row,col]==arr[row,col+1],
                          arr[row,col+1]>0]):
                    arr[row,col]*=2
                    # enable random tile creation
                    self.need_random_tile=True
                    arr[row,col+1]=0
                    self.roll_left(arr)
                else:
                    col+=1
                    continue
            row+=1
        return arr

        
    @logged(logging.DEBUG)        
    def step(self, action):
        '''
            creating step command similar to Q-Learning.
            should return:-
            s1,r,d,_ = env.step(action) 
            s1 - state of the game we need to identify .
            I think this should be index of the maximum value of the tile.
            e.g. if the maximum tile is at the 2nd row,fourth position return 8 and so on
            
            r = reward, score of the game - does it need to be normalized? trying for that.
            So, 2 will get reward of 2/2048 = 0.0009765625
                2048 will get reward of 1.
            
            d = game status dead or alive. the code expect dead to be false which is opposite of
                GAME class which has running = True. So returning not game.running makes sense
                
            action = input action is expected to be one of [0,1,2,3]
        '''
        initial_max_value= max(self.game_state.flatten())
        initial_sum_value=np.sum(self.game_state)
        
        if self.current_move != action:
            self.need_random_tile=True
            self.current_move=action
        
        self.move(action)
        self.add_random_tile()
        self.need_random_tile=False
        self.update_view()
        reward = max(self.game_state.flatten())-initial_max_value
        sum_val=np.sum(self.game_state)
        reward=sum_val-initial_sum_value
        reward=sum_val
        dead = not self.running
        
        return self.get_state_list(),reward,dead,None
        pass
    
    def get_state_list(self):
        game_list=self.game_state.flatten().tolist()
        max_list=[list((i,v)) for i,v in enumerate(game_list) if v==max(game_list)]
        max_list=[item for sublist in max_list for item in sublist]
        if len(max_list)<4:
            max_list[2:4]=[0]*2
        return max_list[0:4]
        pass
    
    @logged(logging.DEBUG)        
    def get_state(self):
        state_list=self.game_state.flatten()
        maxVIndex= [i for i,v in enumerate(state_list) if v==max(state_list)]
        return self.game_state.flatten()
    
    @logged(logging.DEBUG)        
    def initialize_game_state(self):
        self.game_state=np.zeros((NUMBER_OF_TILE,NUMBER_OF_TILE))
        self.game_state=self.game_state.astype(int)
        self.running=True
        self.win=False
        
    
    @logged(logging.DEBUG)        
    def reset(self):
        if GAME_MODE=="live":
            self.game_box.banner=""
            self.game_box.game_over()
            
        self.current_move=-1
        self.need_random_tile=True
        self.initialize_game_state()
        self.seed()
        self.update_view()
        return self.get_state_list()
    
    @logged(logging.DEBUG)        
    def action_space_sample(self):
        return randrange(4)
    
    @logged(logging.DEBUG)        
    def seed(self):
        self.add_random_tile() # first random tile
        self.add_random_tile() # second random tile
        self.need_random_tile=True
        self.update_view()
    
    @logged(logging.DEBUG)        
    def update_game_score(self):
        max_v=np.amax(self.game_state)
        if max_v!=2:
            self.score=max_v
        if GAME_MODE=="live":
            self.score_board.score=self.score
        
    @logged(logging.DEBUG)        
    def quit(self):
        self.running=False
        if GAME_MODE=="live":
            pygame.quit()
    
    @logged(logging.DEBUG)        
    def update_view(self):
        self.update_game_score()
        self.check_game_status()
        if GAME_MODE=="live":
            pygame.event.pump()
            self.tile_group.empty()
            for row in range(NUMBER_OF_TILE):
                for col in range(NUMBER_OF_TILE):
                    self.tile_group.add(row,col,self.game_state[row,col])
            self.tile_group.draw(self.screen)
            self.score_board.update_score()
            pygame.display.update()
            

    @logged(logging.DEBUG)        
    def check_game_status(self):
        """
        Check Game Status
        Returns Boolean
        -------
        TYPE
            DESCRIPTION.
        """
        # --- model---
        if self.score==2048:
            self.running=False
            self.win=True
        elif np.all(self.game_state):
            if all([np.amin(np.absolute(np.diff(self.game_state,axis=1)))>0,
                    np.amin(np.absolute(np.diff(self.game_state,axis=0)))>0]):
                self.running=False
                self.win=False

        # --- view ---
        if GAME_MODE=="live":
            if self.score==2048:
                self.game_box.banner="You Won!"
                self.game_box.game_over()
            elif np.all(self.game_state):
                if all([np.amin(np.absolute(np.diff(self.game_state,axis=1)))>0,
                        np.amin(np.absolute(np.diff(self.game_state,axis=0)))>0]):
                    self.game_box.game_over()
        return self.win
            
                
    
    @logged(logging.DEBUG)        
    def add_random_tile(self):
        """
        If random tiles are needed - add a random tile
        Returns
        -------
        None.
        """
        if self.need_random_tile:
            iterator=0
            while True:
                r=randrange(4)
                c=randrange(4)
                if self.game_state[r,c]!=0:
                    iterator+=1
                    continue
                elif np.all(self.game_state):
                    self.running=False
                    self.win=False                
                    break
                else:
                    self.game_state[r,c]=2
                    break
    
#---------------Movements-------------------------------------------------
    def move(self,direction_val):
        """
        Parameters
        ----------
        direction_val : integer
            DESCRIPTION.
            0=left
            1=right
            2=down
            3=up

        Returns
        -------
        None.
        """
        direction_list=["left","right","down","up"]
        direction=direction_list[direction_val]
        
        arr=self.game_state
        
        if direction=="up":
            arr=np.transpose(arr)
        elif direction=="down":
            arr=np.flip(np.transpose(arr),axis=1)
        elif direction=='right':
            arr=np.flip(arr,axis=1)
        #----------------------------------------
        arr=self.roll_left(arr)
        #----------------------------------------
        if direction=="up":
            arr=np.transpose(arr)
        elif direction=="down":
            arr=np.transpose(np.flip(arr,axis=1))
        elif direction=='right':
            arr=np.flip(arr,axis=1)
        
        self.game_state=arr
        pass


def main():
    clock = pygame.time.Clock()
    game=Game_2048()
    move_list=[pygame.K_LEFT,
               pygame.K_RIGHT,
               pygame.K_DOWN,
               pygame.K_UP]
    
    while game.running and GAME_MODE=="live":
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                game.running = 0
            elif e.type == pygame.KEYDOWN:
                try:
                    game.step(move_list.index(e.key))
                except:
                    print("This movement for key {} not defined".format(e.key))
            elif e.type == pygame.MOUSEBUTTONDOWN:
                pos=pygame.mouse.get_pos()
                if game.score_board.isOver(pos):
                    print("clicked refresh button")
                    game.reset()
    
        game.check_game_status()
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()


def debug():
    clock = pygame.time.Clock()
    game=Game_2048()
    pass

if __name__=="__main__":
    if GAME_MODE=="live":
        main()
    elif GAME_MODE=="debug":
        print("Loaded the class for debugging")
        debug()

