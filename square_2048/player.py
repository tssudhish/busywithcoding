# -*- coding: utf-8 -*-
import game_2048
import pygame
from random import randrange
import numpy as np
# import tflearn
# from tflearn.layers.core import input_data, dropout, fully_connected
# from tflearn.layers.estimator import regression
# from statistics import median, mean
# from collections import Counter
# import numpy as np


LR = 1e-3
goal_steps = 300
score_requirement = 50
initial_games = 5000



def run_game(game):
    game.refresh()  # reset the game for the run
    game_transcript=[]
    game_score_transcript=[]
    
    def player_move(idx,game):
        if idx==0:
            game.move_left()
        elif idx==1:
            game.move_right()
        elif idx==2:
            game.move_down()
        elif idx==3:
            game.move_up()

    print("-"*50)
    move_counter=0
    while game.running:
        pygame.event.pump()
        move=randrange(4)
        action = np.zeros(4).astype(int)
        action[move]=1
        transaction=np.vstack((game.game_state,action))
        player_move(move,game)  
        game.check_game_status()
        move_counter+=1
        pygame.display.update()
        print("-"*50)
        print("Current move number:{} - game score is:{}".format(move_counter,game.score))
        #print(game.game_state)
        print(transaction)
        print(game.running)
        game_transcript.append(transaction)
        game_score_transcript.append(game.score)
        if not game.running:
            pygame.quit()
    return game_transcript, game_score_transcript
score_requirement=2048

# def generate_population(model):
#     # [OBS, MOVES]
#     global score_requirement
#     training_data = []
#     # all scores:
#     scores = []
#     # just the scores that met our threshold:
#     accepted_scores = []
#     # iterate through however many games we want:
#     print('Score Requirement:', score_requirement)
#     for _ in range(initial_games):
#         print('Simulation ', _, " out of ", str(initial_games), '\r', end='')
#         # reset game to play again
#         game.refresh()
#         score = 0
#         # moves specifically from this environment:
#         game_memory = []
#         # previous observation that we saw
#         prev_observation = []
#         # for each frame in 200
#         for _ in range(goal_steps):
#             # choose random action (0 or 1)
#             if len(prev_observation) == 0:
#                 action = random.randrange(0, 3)
#             else:
#                 if not model:
#                     action = random.randrange(0, 3)
#                 else:
#                     prediction = model.predict(prev_observation.reshape(-1, len(prev_observation), 1))
#                     action = np.argmax(prediction[0])
 
#             # do it!
#             game_state, reward, done, info = game.step(action)
 
#             # notice that the observation is returned FROM the action
#             # so we'll store the previous observation here, pairing
#             # the prev observation to the action we'll take.
#             if len(prev_observation) > 0:
#                 game_memory.append([prev_observation, action])
#             prev_observation = observation
#             score += reward
#             if done: break
 
#         # IF our score is higher than our threshold, we'd like to save
#         # every move we made
#         # NOTE the reinforcement methodology here.
#         # all we're doing is reinforcing the score, we're not trying
#         # to influence the machine in any way as to HOW that score is
#         # reached.
#         if score >= score_requirement:
#             accepted_scores.append(score)
#             for data in game_memory:
#                 # convert to one-hot (this is the output layer for our neural network)
 
#                 action_sample = [0, 0, 0]
#                 action_sample[data[1]] = 1
#                 output = action_sample
#                 # saving our training data
#                 training_data.append([data[0], output])
 
#         # save overall scores
#         scores.append(score)
 
#     # some stats here, to further illustrate the neural network magic!
#     print('Average accepted score:', mean(accepted_scores))
#     print('Score Requirement:', score_requirement)
#     print('Median score for accepted scores:', median(accepted_scores))
#     print(Counter(accepted_scores))
#     score_requirement = mean(accepted_scores)
 
#     # just in case you wanted to reference later
#     training_data_save = np.array([training_data, score_requirement])
#     np.save('saved.npy', training_data_save)
 
#     return training_data
 
    
 

if __name__ == "__main__":
    game=game_2048.GAME()
    X, Y = run_game(game)
    #training_data = generate_population(None)