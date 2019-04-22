import numpy as np
import utils
import random
import math


class Agent:

    def __init__(self, actions, Ne, C, gamma):
        self.actions = actions
        self.Ne = Ne  # used in exploration function
        self.C = C
        self.gamma = gamma

        # Create the Q and N Table to work with
        self.Q = utils.create_q_table()
        self.N = utils.create_q_table()
        self.reset()

    def train(self):
        self._train = True

    def eval(self):
        self._train = False

    # At the end of training save the trained model
    def save_model(self, model_path):
        utils.save(model_path, self.Q)

    # Load the trained model for evaluation
    def load_model(self, model_path):
        self.Q = utils.load(model_path)

    def reset(self):
        self.points = 0
        self.s = None
        self.a = None

    def updateState(self, state):
        snake_head_x, snake_head_y, snake_body, food_x, food_y = state
        snake_head_x = math.floor(snake_head_x/40)
        snake_head_y = math.floor(snake_head_y/40)
        tmp = []
        for i, j in snake_body:
            tmp.append((math.floor(i/40), math.floor(j/40)))
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
        if ((snake_head_x, snake_head_y-1) in tmp):
            ret = 1
        else:
            ret = 0
        adjoining_body.append(ret)
        if ((snake_head_x, snake_head_y+1) in tmp):
            ret = 1
        else:
            ret = 0
        adjoining_body.append(ret)
        if ((snake_head_x-1, snake_head_y) in tmp):
            ret = 1
        else:
            ret = 0
        adjoining_body.append(ret)
        if ((snake_head_x+1, snake_head_y) in tmp):
            ret = 1
        else:
            ret = 0
        adjoining_body.append(ret)
        return (adjoining_wall[0], adjoining_wall[1], food_dir[0], food_dir[1], adjoining_body[0], adjoining_body[1], adjoining_body[2], adjoining_body[3])

    def updateQtable(self, last_move_state, last_move_action, state, dead, points):
        last_move = self.updateState(last_move_state)

        if points - self.points > 0:
            reward = 1
        elif dead:
            reward = -1
        else:
            reward = -0.1

        curr = self.updateState(state)
        upper = self.Q[curr[0]][curr[1]][curr[2]][curr[3]][curr[4]][curr[5]][curr[6]][curr[7]][0]
        bottom = self.Q[curr[0]][curr[1]][curr[2]][curr[3]][curr[4]][curr[5]][curr[6]][curr[7]][1]
        left = self.Q[curr[0]][curr[1]][curr[2]][curr[3]][curr[4]][curr[5]][curr[6]][curr[7]][2]
        right = self.Q[curr[0]][curr[1]][curr[2]][curr[3]][curr[4]][curr[5]][curr[6]][curr[7]][3]
        max_a = max(upper, bottom, left, right)
        alpha = self.C / (self.C + self.N[last_move[0]][last_move[1]][last_move[2]][last_move[3]]
                          [last_move[4]][last_move[5]][last_move[6]][last_move[7]][last_move_action])

        Q_val = self.Q[last_move[0]][last_move[1]][last_move[2]][last_move[3]][last_move[4]][last_move[5]][last_move[6]][last_move[7]][last_move_action]
        return Q_val + alpha * (reward + self.gamma * max_a - Q_val)

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
        tmp = state.copy()
        tmp[2] = state[2].copy()

        curr_state = self.updateState(state)
        if dead:
            last_move_state = self.updateState(self.s)
            self.Q[last_move_state[0]][last_move_state[1]][last_move_state[2]][last_move_state[3]][last_move_state[4]][last_move_state[5]][last_move_state[6]][last_move_state[7]][self.a] = self.updateQtable(self.s, self.a, state, dead, points)
            self.reset()
            return

        if self.s != None and self.a != None and self._train:
            last_move_state = self.updateState(self.s)
            new_q = self.updateQtable(self.s, self.a, state, dead, points)
            self.Q[last_move_state[0]][last_move_state[1]][last_move_state[2]][last_move_state[3]][last_move_state[4]][last_move_state[5]][last_move_state[6]][last_move_state[7]][self.a] = new_q

        # it should return the last one if there is a tie of argmax
        utility = [0, 0, 0, 0]
        for i in range(4):
            N_val = self.N[curr_state[0]][curr_state[1]][curr_state[2]][curr_state[3]][curr_state[4]][curr_state[5]][curr_state[6]][curr_state[7]][i]
            Q_val = self.Q[curr_state[0]][curr_state[1]][curr_state[2]][curr_state[3]][curr_state[4]][curr_state[5]][curr_state[6]][curr_state[7]][i]
            if N_val < self.Ne:
                utility[i] = 1
            else:
                utility[i] = Q_val

        action = np.argmax(utility)
        max_action = max(utility)
        for i in range(len(utility)-1, -1, -1):
            if utility[i] == max_action:
                action = i
                break

        self.N[curr_state[0]][curr_state[1]][curr_state[2]][curr_state[3]][curr_state[4]][curr_state[5]][curr_state[6]][curr_state[7]][action] += 1
        # discretized state should be passed
        # deep copy
        self.s = tmp
        self.s[2] = tmp[2].copy()
        self.a = action
        self.points = points
        return action
