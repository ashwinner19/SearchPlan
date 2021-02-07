import numpy as np
from game import Player
import random
from tqdm import tqdm
import pygame
import constants
import json
import matplotlib.pyplot as plt
from Q_learning import Q_learning
#from SARSA_tabular import SARSA


MAP_WID=50
MAP_HEI=50

episodes = 1000
alpha = 0.7
epsilon = 0.2
gamma =0.9
initial_state = 'No'


steps_q_learning,rewards_q_learning,final_states_q_learning,map_details,target_q_learning = Q_learning(episodes,alpha,epsilon,gamma,initial_state)


plt.title('Steps per episode for 300 episodes and 1 run')
plt.ylabel('Steps')
plt.xlabel('Episodes')
plt.plot(steps_q_learning,label = 'Q-learning')
plt.legend()
plt.show()



plt.title('Reward per episode for 300 episodes and 1 run')
plt.ylabel('rewards')
plt.xlabel('Episodes')
plt.plot(rewards_q_learning,label = 'Q-learning')
plt.legend()
plt.show()


SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
for i in range(len(final_states_q_learning)):
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Q-learning')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill((0, 0, 0))
    for x in range(0, MAP_WID):
        for y in range(0, MAP_HEI):
            if map_details[x][y] == 'true':
                screen.blit(constants.WALL, (x * 10, y * 10))
            else:
                screen.blit(constants.FLOOR, (x * 10, y * 10))
            
    
    pygame.draw.rect(screen,(250,250,250),(final_states_q_learning[i][0]*10,final_states_q_learning[i][1] * 10,10,10))
    for i in range(len(target_q_learning)):
        pygame.draw.rect(screen,(100,100,100),(target_q_learning[i][0]*10,target_q_learning[i][1]*10,10,10))
    pygame.display.flip()

