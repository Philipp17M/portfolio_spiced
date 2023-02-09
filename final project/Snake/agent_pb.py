#from snake_env import Snake
from Snake_env import Snake_game

import random
import numpy as np
from keras import Sequential
from collections import deque
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten, BatchNormalization
import matplotlib.pyplot as plt
from keras.optimizers import Adam
from plot_script import plot_result
import time
from keras import backend as k
import os
import pandas as pd


class DQN:

    """ Deep Q Network """

    def __init__(self, env, params):

        self.action_space = env.action_space
        self.state_space = env.state_space
        self.architecture = env.architecture
        self.epsilon = params['epsilon'] 
        self.gamma = params['gamma'] 
        self.gamma_gain = params['gamma_gain']
        self.gamma_start = params['gamma_start']
        self.gamma_max = params['gamma_max']
        self.batch_size = params['batch_size'] 
        self.epsilon_min = params['epsilon_min'] 
        self.epsilon_decay = params['epsilon_decay'] 
        self.learning_rate = params['learning_rate']
        self.layer_sizes = params['layer_sizes']
        self.memory = deque(maxlen=2500)
        self.model = self.build_model()


    def build_model(self):
        k.clear_session()
        
        if self.architecture == 'complex_cnn':
            model = Sequential([
            Conv2D(16, kernel_size=(3, 3), strides=(3, 3),
                padding="same", activation="relu",
                input_shape=self.state_space),
            MaxPooling2D(pool_size=(3, 3), strides=(3, 3), padding="same"),
            Conv2D(32, kernel_size=(3, 3), strides=(3, 3),
                padding="same", activation="relu",
                ),
            MaxPooling2D(pool_size=(3, 3), strides=(2, 2), padding="same"),    
            #BatchNormalization(),
            Flatten(),
            Dense(units = 128, activation = 'relu'),
            Dense(units = 32, activation = 'relu'),
            Dense(units = self.action_space, activation = 'linear')
            ])
            model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
            model.summary()

        elif self.architecture == 'simple' or self.architecture == 'complex':
            model = Sequential()
            for i in range(len(self.layer_sizes)):
                if i == 0:
                    model.add(Dense(self.layer_sizes[i], input_shape=(self.state_space,), activation='relu'))
                else:
                    model.add(Dense(self.layer_sizes[i], activation='relu'))
            model.add(Dense(self.action_space, activation='softmax'))
            model.add(Dropout(0.2))
            model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))


        return model


    def remember(self, state, action, reward, next_state, done):
        self.memory.appendleft((state, action, reward, next_state, done))


    def act(self, state):

        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_space)
        if self.architecture == 'complex_cnn':
            act_values = self.model.predict(np.expand_dims(state, 0))
        else:
            act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def backpropagate(self):
        # cast qeue memory as np array
        memory_array = np.array(self.memory, dtype=object)
        # find index of first True after a bunch of Falses (game-over indicator) in list of dones
        game_over_idx = list(memory_array[:,4]).index(True, list(memory_array[:,4]).index(False, 0))
        # backpropagate rewards in time, up to last game-over (game_over_idx)
        previous_rew = 0
        for idx in range(game_over_idx):
            memory_array[idx,2] += self.gamma * previous_rew
            previous_rew = memory_array[idx,2]
        # convert back to deque
        self.memory = deque(memory_array, maxlen=2500)


    def replay(self):

        if len(self.memory) < self.batch_size:
            return
        mem_array = np.array(self.memory, dtype=object)
        mem_array_done = mem_array[mem_array[:,-1] == True]
        mem_array_undone = mem_array[mem_array[:,-1] == False]
        # set 30/70 for game-over and normal steps to speed up the game over learning
        idx_undone = np.random.randint(len(mem_array_undone), size=int(self.batch_size*0.7))
        idx_done = np.random.randint(len(mem_array_done), size=int(self.batch_size*0.3))
        minibatch_1 = mem_array_undone[idx_undone,:]
        minibatch_2 = mem_array_done[idx_done,:]
        #minibatch_1 = random.sample(mem_array_done, self.batch_size//2)
        #minibatch_2 = random.sample(mem_array_undone, self.batch_size//2)
        minibatch = np.concatenate((minibatch_1, minibatch_2), axis=0)
        states = np.array([i[0] for i in minibatch])
        actions = np.array([i[1] for i in minibatch])
        rewards = np.array([i[2] for i in minibatch])
        next_states = np.array([i[3] for i in minibatch])
        dones = np.array([i[4] for i in minibatch])
        
        #minibatch = random.sample(self.memory, self.batch_size)
        #states = np.array([i[0] for i in minibatch])
        #actions = np.array([i[1] for i in minibatch])
        #rewards = np.array([i[2] for i in minibatch])
        #next_states = np.array([i[3] for i in minibatch])
        #dones = np.array([i[4] for i in minibatch])

        states = np.squeeze(states)
        next_states = np.squeeze(next_states)

        targets = rewards# + self.gamma*(np.amax(self.model.predict_on_batch(next_states), axis=1))*(1-dones)
        targets_full = self.model.predict_on_batch(states)
        #targets_full = np.zeros((self.batch_size, 4))

        ind = np.array([i for i in range(self.batch_size)])
        targets_full[[ind], [actions]] = targets

        self.model.fit(states, targets_full, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


def train_dqn(episode, env):
    os.chdir('C:/Users/Philipp/Documents/SPICED/student_code/final_project/Snake/checkpoints')
    sum_of_rewards = []
    track_highscore = []
    agent = DQN(env, params)
    sum_of_steps = 0
    agent.gamma = agent.gamma_start
    for e in range(episode):
        agent.gamma = agent.gamma * agent.gamma_gain
        if agent.gamma > agent.gamma_max:
            agent.gamma = agent.gamma_max
        state = env.reset()
        if env.architecture == 'simple':
            state = np.reshape(state, (1, env.state_space))
        score = 0
        max_steps = 10000
        for i in range(max_steps):
            action = agent.act(state)
            # print(action)
            prev_state = state
            next_state, reward, done, _ = env.step(action)
            score += reward
            if env.architecture == 'simple':
                next_state = np.reshape(next_state, (1, env.state_space))
            if  e==0 and i==0:
                agent.remember(state, action, reward, next_state, True) 
            agent.remember(state, action, reward, next_state, done)
            sum_of_steps += 1
            env.steps_total += 1
            print('Gamma:', agent.gamma, ' Epsilon:', agent.epsilon, ' reward:', env.reward, ' ep:', e, '/', episode, ' steps_sum:', sum_of_steps)
            state = next_state
            if (params['batch_size'] > 1):# and (True if e==0 else (i % e == 0)):
                agent.replay()
            if done:
                print(f'final state before dying: {str(prev_state)}')
                print(f'episode: {e+1}/{episode}, score: {score}')
                agent.backpropagate()
                break
        sum_of_rewards.append(score)
        # make list with acutal snake-score (to track highscore during training)
        track_highscore.append(env.score)
        
        if e % 10 == 0:
            path = './episode '+ str(e) + ' checkpoint'
            agent.model.save_weights(path)
            df_highscore = pd.DataFrame(track_highscore)
            df_highscore.to_pickle(('../scores/complex ep ' + str(e)))
    return sum_of_rewards


if __name__ == '__main__':

    params = dict()
    params['name'] = None
    params['epsilon'] = 1

    params['gamma'] = .9
    params['gamma_gain'] = 1.1
    params['gamma_start'] = 0.05
    params['gamma_max'] = 0.9
    params['batch_size'] = 500
    params['epsilon_min'] = .005
    params['epsilon_decay'] = .99
    params['learning_rate'] = 0.00025
    params['layer_sizes'] = [512, 128]

    results = dict()
    ep = 1000

    # for batchsz in [1, 10, 100, 1000]:
    #     print(batchsz)
    #     params['batch_size'] = batchsz
    #     nm = ''
    #     params['name'] = f'Batchsize {batchsz}'
    env_infos = {'States: only walls':{'state_space':'no body knowledge'}, 'States: direction 0 or 1':{'state_space':''}, 'States: coordinates':{'state_space':'coordinates'}, 'States: no direction':{'state_space':'no direction'}}

    # for key in env_infos.keys():
    #     params['name'] = key
    #     env_info = env_infos[key]
    #     print(env_info)
    #     env = Snake(env_info=env_info)
    env = Snake_game('simple')
    sum_of_rewards = train_dqn(ep, env)
    results[params['name']] = sum_of_rewards
    
    plot_result(results, direct=True, k=20)
    