import os
import pygame
from random import randrange

#import ConfigParser

#Constants
#CONFIG = ConfigParser.ConfigParser()
#CONFIG.readfp(open('game.conf'))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND= (251, 248, 239)
BOXBACKGROUND=(201, 189, 177)
FPS   = 1
SCREEN_WIDTH=400
SCREEN_HEIGHT=600
BOX_WIDTH=360
BOX_HEIGHT=360

TILE_GAP=10
NUMBER_OF_TILE=4 #4X4

move=TILE_GAP/2
x_change=0
y_change=0


COLOR_DICT={"2":(238, 228, 218),
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





class Tile(pygame.sprite.Sprite):
    move_this_tile=False
    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()





# Call this function so the Pygame library can initialize itself
pygame.init()
 
# Create an 800x600 sized screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])



# Game Screen
game_w=SCREEN_WIDTH
game_h=SCREEN_HEIGHT

gameScreen=pygame.Rect(0,0,game_w,game_h)

# Box Screen
box_w=BOX_WIDTH
box_h=BOX_HEIGHT
box_loc_x=(SCREEN_WIDTH-BOX_WIDTH)/2
box_loc_y=(SCREEN_HEIGHT-SCREEN_WIDTH)+box_loc_x
boxScreen=pygame.Rect(box_loc_x,box_loc_y,box_w,box_h)



# Draw a tile
game_origin_x=box_loc_x+TILE_GAP
game_origin_y=box_loc_y+TILE_GAP
tile_w=(BOX_WIDTH-(TILE_GAP*(NUMBER_OF_TILE+1)))/NUMBER_OF_TILE
tile_h=tile_w


tile_sprite_group=pygame.sprite.Group()

for num in range(2):

    tile=Tile(COLOR_DICT["2"],tile_w,tile_h)
    tile.rect.x=game_origin_x+randrange(4)*(tile_w+TILE_GAP)
    tile.rect.y=game_origin_y+randrange(4)*(tile_h+TILE_GAP)
    tile.index=num
    # check if this newly created tile is clashing with another
    tile_sprite_group.add(tile)

    



# Set the title of the window
pygame.display.set_caption('2048')
clock = pygame.time.Clock()
running = True
move_tiles=False
while running:
    screen.fill(BLACK)
    pygame.draw.rect(screen,BACKGROUND,gameScreen) #,border_radius=5
    pygame.draw.rect(screen,BOXBACKGROUND,boxScreen) #,border_radius=5

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change=-move
                y_change=0
                move_tiles=True
            elif event.key == pygame.K_RIGHT:
                x_change=move
                y_change=0
                move_tiles=True
            elif event.key == pygame.K_UP:
                x_change=0
                y_change=-move
                move_tiles=True
            elif event.key == pygame.K_DOWN:
                x_change=0
                y_change=move
                move_tiles=True
            else:
                x_change=y_change=0
                move_tiles=False
                
    tile_sprite_group.draw(screen)
    if move_tiles:
        for t in tile_sprite_group:
            t.move_this_tile=True            
    
    
    for t in tile_sprite_group:
        other_tiles_rect=[tl.rect.inflate(TILE_GAP,TILE_GAP) for tl in tile_sprite_group if tl.rect not in t.rect ]
        while t.move_this_tile:
            print("Moving tile:{}".format(t.index))
            t.rect.move_ip(x_change,y_change)
            boxB=(boxScreen.contains(t.rect.inflate(TILE_GAP,TILE_GAP))==1)
            rectColB=(t.rect.collidelist(other_tiles_rect)>=0)
            
            print("tile.rect.x:{},tile.rect.y:{}, boxB:{}, rectColB:{}".format(t.rect.x,t.rect.y,boxB,rectColB))
            if all([boxB,rectColB]):
                  t.rect.move_ip(-x_change,-y_change)
                  t.move_this_tile=False
                  break
    
    pygame.display.update()    
    clock.tick(FPS)

pygame.quit()