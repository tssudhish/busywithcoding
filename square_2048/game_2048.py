import os
import pygame
import random

#import ConfigParser

#Constants
#CONFIG = ConfigParser.ConfigParser()
#CONFIG.readfp(open('game.conf'))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND= (251, 248, 239)
BOXBACKGROUND=(201, 189, 177)
FPS   = 45
SCREEN_WIDTH=400
SCREEN_HEIGHT=600
BOX_WIDTH=360
BOX_HEIGHT=360

TILE_GAP=10
NUMBER_OF_TILE=4 #4X4

COLOR_DICT={2:(238, 228, 218),
            4:(236,224,200),
            8:(242,177,121),
            16:(245,149,99),
            32:(245,124,95),
            64:(246, 93, 58),
            128:(240,198,95),
            256:(237, 204, 97),
            512:(239, 160, 74),
            1024:(237, 197, 63),
            2048:(238, 194, 46)}





class Tile(pygame.sprite.Sprite):
    moveX=4
    moveY=4

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
    def moveLeft(self):
        self.rect.x+=-self.moveX
    def moveRight(self):
        self.rect.x+=self.moveX
    def moveUp(self):
        self.rect.y+=-self.moveY
    def moveDown(self):
        self.rect.y+=self.moveY
    




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
x=game_origin_x
y=game_origin_y
tile_w=(BOX_WIDTH-(TILE_GAP*(NUMBER_OF_TILE+1)))/NUMBER_OF_TILE
tile_h=tile_w
x_change=0
y_change=0
tile=Tile(WHITE,tile_w,tile_h)
tile.rect.x=x
tile.rect.y=y

tile_list=pygame.sprite.Group()
tile_list.add(tile)




# Set the title of the window
pygame.display.set_caption('2048')
clock = pygame.time.Clock()
running = True


while running:
    screen.fill(BLACK)
    pygame.draw.rect(screen,BACKGROUND,gameScreen) #,border_radius=5
    pygame.draw.rect(screen,BOXBACKGROUND,boxScreen) #,border_radius=5

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                for t in tile_list:
                    t.moveLeft()
            if event.key == pygame.K_RIGHT:
                for t in tile_list:
                    t.moveRight()
            if event.key == pygame.K_UP:
                for t in tile_list:
                    t.moveUp()
            if event.key == pygame.K_DOWN:
                for t in tile_list:
                    t.moveDown()

    tile_list.draw(screen)
  #  tile.draw(screen)
    # Flip screen
    pygame.display.update()    
    
    clock.tick(FPS)

pygame.quit()