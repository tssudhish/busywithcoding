import os
import pygame
from random import randrange
import numpy as np

#import ConfigParser

#Constants
#CONFIG = ConfigParser.ConfigParser()
#CONFIG.readfp(open('game.conf'))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND= (251, 248, 239)
BOXBACKGROUND=(177, 181, 180)
FPS   = 60
SCREEN_WIDTH=400
SCREEN_HEIGHT=600
BOX_WIDTH=360
BOX_HEIGHT=BOX_WIDTH


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
    
    def __init__(self,display_surface):
        print("Created {} of w:{} X h:{}".format(self.__class__.__name__,self.box_w,self.box_h))
        self.display_surface=display_surface
        super().__init__([self.box_w,self.box_h])
        self.fill(self.color)
        self.rect=self.get_rect()
        self.rect.x=self.box_loc_x
        self.rect.y=self.box_loc_y
    def show(self):
        self.display_surface.blit(self,(self.rect.x,self.rect.y))
        pygame.display.update()
        

class SCORE_BOARD(GAME_BOX):
    def __init__(self,display_surface):
        self.color=BACKGROUND
        self.box_h=(SCREEN_HEIGHT-BOX_HEIGHT)/4
        self.box_w=self.box_w
        self.box_loc_y=(SCREEN_HEIGHT-BOX_HEIGHT)/4
        self.score=0
        super().__init__(display_surface)
    
    def get_score(self):
        if not pygame.font.get_init():
            pygame.font.init()
        score_font= pygame.font.SysFont('freesans', 60)      
        score_text=  "{}".format(self.score).rjust(5)        
        self.scoreImage=score_font.render(score_text, False, (0, 0, 0))
        
    def update_score(self):
        self.get_score()
        self.display_surface.blit(self,(self.rect.x,self.rect.y))     # wipe clean with rectangle
        self.display_surface.blit(self.scoreImage,(self.rect.x,self.rect.y)) # insert score
        pygame.display.update()
        


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



class GAME():
    number_of_tiles=NUMBER_OF_TILE
    game_state=np.zeros((NUMBER_OF_TILE,NUMBER_OF_TILE))
    game_state=game_state.astype(int)
    
    [[0 for y in range(NUMBER_OF_TILE) ] \
                 for x in range(NUMBER_OF_TILE)]
    running=False
    score=0
    def __init__(self):
        # Create an SCREEN_WIDTH X SCREEN_HEIGHT sized screen
        print("Initialized {}()".format(self.__class__.__name__))
        
        if not pygame.get_init():
            # Call this function so the Pygame library can initialize itself
            pygame.init()
        if pygame.get_init():
            self.running=True
            pygame.display.set_caption('2048')
        else:
            print("Error!! - Unable to initialize pygame")
            raise EnvironmentError
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.screen.fill(BACKGROUND)
        self.game_box=GAME_BOX(self.screen)
        self.game_box.show()
        self.score_board=SCORE_BOARD(self.screen)
        self.tile_group=TILES()
        self.seed()
        self.need_random_tile=False
    
    def seed(self):
        self.add_random_tile() # first random tile
        self.add_random_tile() # second random tile
        self.update_view()
    
    def update_game_score(self):
        max_v=np.amax(self.game_state)
        if max_v!=2:
            self.score=max_v
        self.score_board.score=self.score
        
            
    
    def update_view(self):
        self.update_game_score()
        self.tile_group.empty()
        for row in range(NUMBER_OF_TILE):
            for col in range(NUMBER_OF_TILE):
                self.tile_group.add(row,col,self.game_state[row,col])
        self.tile_group.draw(self.screen)
        self.score_board.update_score()
        pygame.display.update()
        
    
    def add_random_tile(self):
        iterator=0
        while True:
            r=randrange(4)
            c=randrange(4)
            if self.game_state[r,c]!=0:
                iterator+=1
                continue
            elif iterator==(NUMBER_OF_TILE*NUMBER_OF_TILE - 1):
                print("GAME OVER!")
                break                
            else:
                self.game_state[r,c]=2
                break


#---------------Movements-------------------------------------------------
    def move_left(self):
        self.collect_left()
        if self.need_random_tile:
            self.add_random_tile()
            self.need_random_tile=False
        self.update_view()
        clock.tick(FPS)

    def move_right(self):
        self.collect_right()
        if self.need_random_tile:
            self.add_random_tile()
            self.need_random_tile=False
        self.update_view()
        clock.tick(FPS)

    def move_down(self):
        self.collect_down()
        if self.need_random_tile:
            self.add_random_tile()
            self.need_random_tile=False
        self.update_view()
        clock.tick(FPS)

    def move_up(self):
        self.collect_up()
        if self.need_random_tile:
            self.add_random_tile()
            self.need_random_tile=False
        self.update_view()
        clock.tick(FPS)


    def collect_left(self):
        # update game_state
        row=0
        while row<NUMBER_OF_TILE:
            col=0
            while col<NUMBER_OF_TILE-1:
                
                if not np.any(self.game_state[row,:]):
                    break                
                elif all([self.game_state[row,col]==0, 
                          self.game_state[row,col+1]>0]):
                    self.game_state[row,col]=self.game_state[row,col+1]
                    self.game_state[row,col+1]=0
                    self.need_random_tile=True
                    self.collect_left()
                elif all([self.game_state[row,col]==self.game_state[row,col+1],
                          self.game_state[row,col+1]>0]):
                    self.game_state[row,col]*=2
                    self.game_state[row,col+1]=0
                    self.need_random_tile=True
                    self.collect_left()
                else:
                    col+=1
                    #row-=1
                    continue

            row+=1
            self.update_view()
            clock.tick(FPS)
        
    def collect_right(self):
        # update game_state
        row=0
        while row<NUMBER_OF_TILE:
            col=NUMBER_OF_TILE-1
            while col>0:
                
                if not np.any(self.game_state[row,:]):
                    break                
                elif all([self.game_state[row,col]==0, 
                          self.game_state[row,col-1]>0]):
                    self.game_state[row,col]=self.game_state[row,col-1]
                    self.game_state[row,col-1]=0
                    self.need_random_tile=True
                    self.collect_right()
                elif all([self.game_state[row,col]==self.game_state[row,col-1],
                          self.game_state[row,col-1]>0]):
                    self.game_state[row,col]*=2
                    self.game_state[row,col-1]=0
                    self.need_random_tile=True
                    self.collect_right()
                else:
                    col-=1
                    #row-=1
                    continue

            row+=1
            self.update_view()
            clock.tick(FPS)


    def collect_down(self):
        # update game_state
        col=0
        while col<NUMBER_OF_TILE:
            row=NUMBER_OF_TILE-1
            while row>0:
                
                if not np.any(self.game_state[:,col]):
                    break                
                elif all([self.game_state[row,col]==0, 
                          self.game_state[row-1,col]>0]):
                    self.game_state[row,col]=self.game_state[row-1,col]
                    self.game_state[row-1,col]=0
                    self.need_random_tile=True
                    self.collect_down()
                elif all([self.game_state[row,col]==self.game_state[row-1,col],
                          self.game_state[row-1,col]>0]):
                    self.game_state[row,col]*=2
                    self.game_state[row-1,col]=0
                    self.need_random_tile=True
                    self.collect_down()
                else:
                    row-=1
                    #row-=1
                    continue
            col+=1
            self.update_view()
            clock.tick(FPS)


    def collect_up(self):
        # update game_state
        col=0
        while col<NUMBER_OF_TILE:
            row=0
            while row<NUMBER_OF_TILE-1:
                
                if not np.any(self.game_state[:,col]):
                    break                
                elif all([self.game_state[row,col]==0, 
                          self.game_state[row+1,col]>0]):
                    self.game_state[row,col]=self.game_state[row+1,col]
                    self.game_state[row+1,col]=0
                    self.need_random_tile=True
                    self.collect_up()
                elif all([self.game_state[row,col]==self.game_state[row+1,col],
                          self.game_state[row+1,col]>0]):
                    self.game_state[row,col]*=2
                    self.game_state[row+1,col]=0
                    self.need_random_tile=True
                    self.collect_up()
                else:
                    row+=1
                    #row-=1
                    continue
            col+=1
            self.update_view()
            clock.tick(FPS)


clock = pygame.time.Clock()
game=GAME()
#while game.running:
#    for e in pygame.event.get():
#        if e.type == pygame.QUIT:
#            game.running = 0


#game.clear()

pygame.display.update()
clock.tick(FPS)



#pygame.quit()






 







#while running:
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            pygame.quit()

#pygame.display.update()


#
## Game Screen
#game_w=SCREEN_WIDTH
#game_h=SCREEN_HEIGHT
#
#gameScreen=pygame.Rect(0,0,game_w,game_h)
#
## Box Screen
#box_w=BOX_WIDTH
#box_h=BOX_HEIGHT
#box_loc_x=(SCREEN_WIDTH-BOX_WIDTH)/2
#box_loc_y=(SCREEN_HEIGHT-SCREEN_WIDTH)+box_loc_x
#boxScreen=pygame.Rect(box_loc_x,box_loc_y,box_w,box_h)
#
#
#
## Draw a tile
#game_origin_x=box_loc_x+TILE_GAP
#game_origin_y=box_loc_y+TILE_GAP
#
#
#
#tile_sprite_group=pygame.sprite.Group()
#
#for num in range(2):
#
#    tile=Tile(COLOR_DICT["2"],tile_w,tile_h)
#    tile.rect.x=game_origin_x+randrange(4)*(tile_w+TILE_GAP)
#    tile.rect.y=game_origin_y+randrange(4)*(tile_h+TILE_GAP)
#    tile.index=num
#    # check if this newly created tile is clashing with another
#    tile_sprite_group.add(tile)
#
#    
#
#
#
## Set the title of the window
#pygame.display.set_caption('2048')
#clock = pygame.time.Clock()
#running = True
#move_tiles=False
#while running:
#    screen.fill(BLACK)
#    pygame.draw.rect(screen,BACKGROUND,gameScreen) #,border_radius=5
#    pygame.draw.rect(screen,BOXBACKGROUND,boxScreen) #,border_radius=5
#
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            running = False
#        if event.type == pygame.KEYDOWN:
#            if event.key == pygame.K_LEFT:
#                x_change=-move
#                y_change=0
#                move_tiles=True
#            elif event.key == pygame.K_RIGHT:
#                x_change=move
#                y_change=0
#                move_tiles=True
#            elif event.key == pygame.K_UP:
#                x_change=0
#                y_change=-move
#                move_tiles=True
#            elif event.key == pygame.K_DOWN:
#                x_change=0
#                y_change=move
#                move_tiles=True
#            else:
#                x_change=y_change=0
#                move_tiles=False
#                
#    tile_sprite_group.draw(screen)
#    if move_tiles:
#        for t in tile_sprite_group:
#            t.move_this_tile=True            
#    
#    
#    for t in tile_sprite_group:
#        other_tiles_rect=[tl.rect.inflate(TILE_GAP,TILE_GAP) for tl in tile_sprite_group if tl.rect not in t.rect ]
#        while t.move_this_tile:
#            print("Moving tile:{}".format(t.index))
#            t.rect.move_ip(x_change,y_change)
#            boxB=(boxScreen.contains(t.rect.inflate(TILE_GAP,TILE_GAP))==1)
#            rectColB=(t.rect.collidelist(other_tiles_rect)>=0)
#            
#            print("tile.rect.x:{},tile.rect.y:{}, boxB:{}, rectColB:{}".format(t.rect.x,t.rect.y,boxB,rectColB))
#            if all([boxB,rectColB]):
#                  t.rect.move_ip(-x_change,-y_change)
#                  t.move_this_tile=False
#                  break
#    
#    pygame.display.update()    
#    clock.tick(FPS)
#
#pygame.quit()