import numpy as np
from game import Player
import random
from tqdm import tqdm
import pygame
import constants
import json
import matplotlib.pyplot as plt
#from reward import reward,get_rewatd_table
from reward import reward
from target_generation import agent_subgoal_position_generation


player =Player()
game_state_generation =agent_subgoal_position_generation()
MAP_WID=50
MAP_HEI=50

def action_selection(Q,epsilon,position):
    if np.random.random() < epsilon:
        return player.actions[np.random.choice(len(player.actions))]
    else:
        return player.actions[np.argmax(Q[position])]


def Q_learning(episodes,alpha,epsilon,gamma,initial_state):
    START_EPSILON_DECAYING = 2
    END_EPSILON_DECAYING =  episodes
    epsilon_decay = epsilon / (END_EPSILON_DECAYING - START_EPSILON_DECAYING)
    Q_table = np.ones([(MAP_HEI*MAP_WID), len(player.actions)])
    Q_tab_pos_dic = {}
    z = 0
    for i in range(MAP_WID):
        for j in range(MAP_HEI):
            Q_tab_pos_dic[(i,j)] = z
            z+=1
    initial=game_state_generation.initial_state()
    sub= game_state_generation.random_target()
    print("Done_generating",initial,sub)
    length_of_episode = np.zeros(episodes)
    episode_rewards = np.zeros(episodes)
    for i in tqdm(range(episodes)):
        #reward_table = get_rewatd_table()
        all_traversed_state =[]
        player.goal_reached=False
        in_map_p = True
        if initial_state == 'fixed':
            current_state = [40,14]#[26, 20]#
        else:
            current_state = initial
        #target = [12, 34]
        #subgoal = [[37, 19],[29, 17],[29,7],[10,19]]
        subgoal = sub
        target_sent= subgoal
        number_of_subgoals=5
        subgoal_count = 0
        prev_subgoal_count=0
        visited=[]
        t = 0
        running = True
        while running:
            t += 1 
            all_traversed_state.append(current_state)
            index_q_old = Q_tab_pos_dic.get((current_state[0],current_state[1]))
            action = action_selection(Q_table,epsilon,index_q_old)
            #new_state,goal_reached,wall_reward = player.move(current_state,action,target,subgoal_count,t)
            new_state,goal_reached = player.move(current_state,action,subgoal_count,t)
            #current_reward,subgoal_count,visited = reward(target,new_state,subgoal,subgoal_count,gamma,prev_subgoal_count,visited,number_of_subgoals)
            current_reward,subgoal_count,visited = reward(new_state,subgoal,subgoal_count,gamma,prev_subgoal_count,visited,number_of_subgoals)
            episode_rewards[i] += current_reward
            action_index = player.actions.index(action)
            index_q_new = Q_tab_pos_dic.get((new_state[0],new_state[1]))
            Q_table[index_q_old][action_index] = (1-alpha)*Q_table[index_q_old][action_index] + alpha * (current_reward + gamma * np.max(Q_table[index_q_new]) - Q_table[index_q_old][action_index])
            current_state = new_state
            if goal_reached == True:
                running = False
            epsilon-=epsilon_decay
            prev_subgoal_count=subgoal_count
        length_of_episode[i] = t
    print(length_of_episode)
    print(visited)
    import pandas as pd 
    pd.DataFrame(Q_table).to_csv("Q_table.csv")
    print(Q_table)
    return length_of_episode,episode_rewards,all_traversed_state,player.map_dat,target_sent
