#!/usr/bin/env python
# coding: utf-8

import numpy as np
import gym
import seaborn as sns
import pandas as pd
import tensorflow as tf
sns.set()

"""
# ***
# ### $Q$-learning as a Regression Problem
# 
# When we first learned about $Q$-learning, we used the Bellman equation to learn the $Q$ function:
# $$
# Q(s_t, a_t) \gets Q(s_t, a_t) + \alpha \left( r_t + (1-d_t)\gamma \max_{a_{t+1}} \left( Q(s_{t+1}, a_{t+1}) \right) - Q(s_t, a_t) \right)
# $$
# 
# Compare this to gradient descent for a regression problem:
# $$
# \theta \gets \theta - \alpha 2 \left( \hat{y} - y \right) \nabla_\theta \hat{y}
# $$
# 
# These methods are essentially analogous: we update parameters about our function in a manner proportional to the difference between our prediction and the 'true' value. The difference for tabular $Q$-learning is that we essentially have a different parameter for each state-action pair. 
# 
# If we define the following loss function:
# $$
# L(\theta) = \frac{1}{2} \left( r_t + (1-d_t)\gamma \max_{a_{t+1}} \left( Q(s_{t+1}, a_{t+1}) \right) - Q(s_t, a_t) \right)^2
# $$
# 
# Then the gradient descent update rule is exactly the same as our q-learning update rule!
# 
# ### FrozenLake with Tensorflow
# 
# Before diving deep into using techniques like deep neural networks, I want to show you how we might do $Q$-learning in tensorflow using the same `FrozenLake-v0` environment from earlier.
"""

class Agent:
    """
    Reinforcement Learning Agent
    """
    def __init__(self, num_states, num_actions, 
                 epsilon_i=1.0, 
                 epsilon_f=0.0, 
                 n_epsilon=0.1, 
                 alpha=0.1, 
                 gamma = 0.95,
                 hidden_layers = []
                ):
        """
        

        Parameters
        ----------
        num_states : TYPE
            DESCRIPTION.
        num_actions : TYPE
            DESCRIPTION.
        epsilon_i : TYPE, optional
            DESCRIPTION. The default is 1.0.
        epsilon_f : TYPE, optional
            DESCRIPTION. The default is 0.0.
        n_epsilon : TYPE, optional
            DESCRIPTION. The default is 0.1.
        alpha : TYPE, optional
            DESCRIPTION. The default is 0.5.
        gamma : TYPE, optional
            DESCRIPTION. The default is 0.95.
        hidden_layers : TYPE, optional
            DESCRIPTION. The default is [].

        Returns
        -------
        None.

        """
        self.epsilon_i = epsilon_i
        self.epsilon_f = epsilon_f
        self.epsilon = epsilon_i
        self.n_epsilon = n_epsilon
        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.Q = tf.Variable(tf.zeros((num_states, num_actions)), name="Q")
        self.optimizer = tf.keras.optimizers.SGD(alpha)

    def decay_epsilon(self, n):
        """
        

        Parameters
        ----------
        n : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.epsilon = max(
            self.epsilon_f, 
            self.epsilon_i - (n/self.n_epsilon)*(self.epsilon_i - self.epsilon_f))
    
    def act(self, s_t):
        """
        

        Parameters
        ----------
        s_t : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
#         print("np.random.rand(): {} < self.epsilon: {}".format(np.random.rand(),self.epsilon))
        action=-1
        if np.random.rand() < self.epsilon:
            action= np.random.randint(self.num_actions)
            print("Random Action selected : {}".format(action))
        else:
#             max_v_current=[i for i,val in enumerate(s_t) if val == s_t.max()][0]
            print(self.Q)
#             print("np.argmax(self.Q[max_v_current]) = {}".format(np.argmax(self.Q[max_v_current])))
#             print(np.argmax(self.Q.numpy(), axis=0))
            action= np.argmax(np.argmax(self.Q.numpy(), axis=0))
            
            #np.argmax(self.Q[max_v_current])
            print("Predicted Action selected : {}".format(action))
#         print("Action = {}".format(action))
#         print(self.Q)
        return action
    
    def update(self, s_t, a_t, r_t, s_t_next, d_t):
#         print("------------- update -------------")
#         print("*"*50)
#         print(s_t)
#         print("*"*50)
#         print(a_t)
#         print("*"*50)
#         print(r_t)
#         print("*"*50)
#         print("-------------s_t_next-------------")
#         print(s_t_next.transpose())
#         print("*"*50)
#         print("-------------d_t     -------------")
#         print(d_t)
        
#         print("*"*50)
#         print(self.Q[[i for i,val in enumerate(s_t_next) if val == s_t_next.max()][0]])
        max_v_next=[i for i,val in enumerate(s_t_next) if val == s_t_next.max()][0]
        max_v_current=[i for i,val in enumerate(s_t) if val == s_t.max()][0]
#         print("*"*50)
#         print(np.max(self.Q[max_v_next]))
        Q_next = tf.stop_gradient(np.max(self.Q[max_v_next]))
        with tf.GradientTape() as tape:
            loss = 0.5*tf.reduce_mean(r_t + (1-d_t)*self.gamma*Q_next -  self.Q[max_v_current, a_t])**2
        grads = tape.gradient(loss, [self.Q])
        self.optimizer.apply_gradients(zip(grads, [self.Q]))
        


# In[3]:


def plot(data, window=100):
    sns.lineplot(
        data=data.rolling(window=window).mean()[window-1::window]
    )


# In[7]:


def train(env,
         T=100000, alpha=0.8, gamma=0.95, epsilon_i = 1.0, epsilon_f = 0.0, n_epsilon = 0.1):
#    env = gym.make(env_name)
#    num_states = env.observation_space.n
#    num_actions = env.action_space.n
    num_states=len(env.reset())
    num_actions=4
    agent = Agent(num_states, num_actions, alpha=alpha, gamma=gamma, epsilon_i=epsilon_i, epsilon_f=epsilon_f, n_epsilon = n_epsilon)
    
#     print(agent.Q)
    rewards = []
    episode_rewards = 0
    
    s_t_act = env.reset()
    s_t=s_t_act/np.max(s_t_act)
    
#     print(s_t)
    for t in range(T):
        print("Iteration: {}".format(t))
#         print(agent.Q)
        a_t = agent.act(s_t)
#         print("Action: {}".format(a_t))
        s_t_next_act, r_t, d_t, info = env.step(a_t)
        s_t_next=s_t_next_act/np.max(s_t_next_act)
#         print("{}\n{}".format("-"*50,s_t_next))
#         print("{}\n{}".format("-"*50,r_t))
#         print(env.game_state)
        agent.update(s_t, a_t, r_t, s_t_next, d_t)
        agent.decay_epsilon(t/T)
        s_t = s_t_next
        episode_rewards += r_t
#         print("Episode Reward: {}".format(episode_rewards))
#         print("Game is dead? {}".format(d_t))
        if d_t:
            print("saving current episode rewards")
            rewards.append(episode_rewards)
            episode_rewards = 0
            s_t_act = env.reset()
            s_t=s_t_act/np.max(s_t_act)
            
    plot(pd.DataFrame(rewards))
    return agent


# In[ ]:


from importlib import reload
import game_2048
game_2048.GAME_MODE='training'
env =game_2048.Game_2048()

train(env, T=1000)


# In[ ]:


# rewards


# In[ ]:


# np.normalize(env.reset())


# In[ ]:




