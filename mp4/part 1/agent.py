import numpy as np
import utils
import random
import math


class Agent:
    
    def __init__(self, actions, Ne, C, gamma):
        self.actions = actions
        self.Ne = Ne # used in exploration function
        self.C = C
        self.gamma = gamma

        # Create the Q and N Table to work with
        self.Q = utils.create_q_table()
        self.N = utils.create_q_table()

    def train(self):
        self._train = True
        
    def eval(self):
        self._train = False

    # At the end of training save the trained model
    def save_model(self,model_path):
        utils.save(model_path, self.Q)

    # Load the trained model for evaluation
    def load_model(self,model_path):
        self.Q = utils.load(model_path)

    def reset(self):
        self.points = 0
        self.s = None
        self.a = None

    def act(self, state, points, dead):
        '''
        :param state: a list of [snake_head_x, snake_head_y, snake_body, food_x, food_y] from environment.
        :param points: float, the current points from environment
        :param dead: boolean, if the snake is dead
        :return: the index of action. 0,1,2,3 indicates up,down,left,right separately

        TODO: write your function here.
        Return the index of action the snake needs to take, according to the state and points known from environment.
        Tips: you need to discretize the state to the state space defined on the webpage first.
        (Note that [adjoining_wall_x=0, adjoining_wall_y=0] is also the case when snake runs out of the 480x480 board)

        '''
        snake_head_x, snake_head_y, snake_body, food_x, food_y = state 
        snake_head_x = math.floor(snake_head_x/40)
        snake_head_y = math.floor(snake_head_y/40)
        snake_body = []
        for i, j in snake_body:
            snake_body.append((math.floor(i/40), math.floor(j/40)))
        food_x = math.floor(food_x/40)
        food_y = math.floor(food_y/40)


        adjoining_wall = [0, 0]
        if snake_head_x == 1:
            adjoining_wall[0] = 1
        elif snake_head_x == 12:
            adjoining_wall[0] = 2
        else:
            adjoining_wall[0] = 0

        if snake_head_y == 1:
            adjoining_wall[1] = 1
        elif snake_head_y == 12:
            adjoining_wall[1] = 2
        else:
            adjoining_wall[1] = 0

        food_dir = [0, 0]
        if (food_x - snake_head_x) > 0:
            food_dir[0] = 2
        elif (food_x - snake_head_x) < 0:
            food_dir[0] = 1
        else:
            food_dir[0] = 0

        if (food_y - snake_head_y) > 0:
            food_dir[1] = 2
        elif (food_y - snake_head_y) < 0:
            food_dir[1] = 1
        else:
            food_dir[1] = 0
            
        adjoining_body = []
        if ((snake_head_x, snake_head_y+1) in snake_body):
            ret = 1
        else:
            ret = 0
        adjoining_body.append(ret)
        if ((snake_head_x, snake_head_y-1) in snake_body):
            ret = 1
        else:
            ret = 0
        adjoining_body.append(ret)
        if ((snake_head_x-1, snake_head_y) in snake_body):
            ret = 1
        else:
            ret = 0
        adjoining_body.append(ret)
        if ((snake_head_x+1, snake_head_y) in snake_body):
            ret = 1
        else:
            ret = 0
        adjoining_body.append(ret)


        return self.actions[0]
