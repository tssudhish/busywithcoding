# -*- coding: utf-8 -*-
import game_2048
import pygame
from random import randrange


game=game_2048.GAME()

def player_move(idx):
    if idx==0:
        game.move_left()
    elif idx==1:
        game.move_right()
    elif idx==2:
        game.move_down()
    elif idx==3:
        game.move_up()
        

print(game.running)
print(game.score)
move_counter=0
while game.running:
    move=randrange(4)
    player_move(move)    
    move_counter+=1
    print("Current move number:{} - game score is:{}".format(move_counter,game.score))
    if move_counter==100:
        game.running=False
        pygame.quit()

    
    
