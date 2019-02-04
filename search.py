# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Rahul Kunji (rahulsk2@illinois.edu) on 01/16/2019

"""
    This is the main entry point for MP1. You should only modify code
    within this file -- the unrevised staff files will be used for all other
    files and classes when code is run, so be careful to not modify anything else.
    """


# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)

import heapq
import queue
from copy import deepcopy

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod)(maze)


def bfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    queue = []
    visited = set()
    queue.append([maze.getStart()])
    while queue:
        cur_path = queue.pop(0)
        cur_row, cur_col = cur_path[-1]
        if (cur_row, cur_col) in visited:
            continue
        visited.add((cur_row, cur_col))
        if maze.isObjective(cur_row, cur_col):
            return cur_path, len(visited)
        for item in maze.getNeighbors(cur_row, cur_col):
            if item not in visited:
                queue.append(cur_path + [item])
    return [], 0


def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    stack = []
    visited = set()
    stack.append([maze.getStart()])
    while stack:
        cur_path = stack.pop(-1)
        cur_row, cur_col = cur_path[-1]
        if (cur_row, cur_col) in visited:
            continue
        visited.add((cur_row, cur_col))
        if maze.isObjective(cur_row, cur_col):
            return cur_path, len(visited)
        for item in maze.getNeighbors(cur_row, cur_col):
            if item not in visited:
                stack.append(cur_path + [item])
    return [], 0


def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    pq = queue.PriorityQueue()
    visited = set()
    result_row, result_col = maze.getObjectives()[0]
    start_row, start_col = maze.getStart()
    # pq item - tuple: (distance, path list)
    cost = abs(start_row-result_row) + abs(start_col - result_col)
    pq.put((cost, [maze.getStart()]))
    while not pq.empty():
        cur_path = pq.get()[1]
        cur_row, cur_col = cur_path[-1]
        if (cur_row, cur_col) in visited:
            continue
        visited.add((cur_row, cur_col))
        if maze.isObjective(cur_row, cur_col):
            return cur_path, len(visited)
        for item in maze.getNeighbors(cur_row, cur_col):
            if item not in visited:
                cost = abs(item[0] - result_row) + abs(item[1] - result_col)
                pq.put((cost, cur_path + [item]))
    return [], 0


# astar for part 1

def astar1(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    pq = queue.PriorityQueue()
    visited = {}
    result_row, result_col = maze.getObjectives()[0]
    start_row, start_col = maze.getStart()
    # pq item - tuple: (distance, path list)
    cost = abs(start_row-result_row) + abs(start_col - result_col)
    pq.put((cost, [maze.getStart()]))
    while not pq.empty():
        cur_path = pq.get()[1]
        cur_row, cur_col = cur_path[-1]
        if (cur_row, cur_col) in visited:
            continue
        cur_cost = abs(cur_row - result_row) + \
            abs(cur_col - result_col) + len(cur_path) - 1
        visited[(cur_row, cur_col)] = cur_cost
        if maze.isObjective(cur_row, cur_col):
            return cur_path, len(visited)
        for item in maze.getNeighbors(cur_row, cur_col):
            new_cost = abs(item[0] - result_row) + \
                abs(item[1] - result_col) + len(cur_path) - 1
            if item not in visited:
                pq.put((new_cost, cur_path + [item]))
            else:
                # if a node that’s already in the explored set found, test to see if the new h(n)+g(n) is smaller than the old one.
                if visited[item] > new_cost:
                    visited[item] = new_cost
                    pq.put((new_cost, cur_path + [item]))
    return [], 0

# ====================================== PART 2 ===============================================
# astar for part 2
#self-built data structure
class ctor:
    def __init__(self, row, col, cost, tcost):
        self.row      = row
        self.col      = col
        self.position = (row, col)
        self.cost     = cost  #heuristic
        self.tcost   = tcost  # f = g + h（total）
        self.prev     = None
        self.not_visited  = []
        self.level = 0
    def __lt__(self, other):
        return self.tcost < other.tcost

def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    if len(maze.getObjectives())==1:
        return astar1(maze)

    start = maze.getStart()
    goals_left = maze.getObjectives()
    goals_left.insert(0,start)
    edge_list = {} 
    heuristic_list = {} 
    #building graph for mst
    for i in goals_left:
        for j in goals_left:
            if i != j:
                construct_path = cost_sofar(i,j, maze)[0]
                edge_list[(i,j)] = construct_path
                heuristic_list[(i,j)] = len(construct_path)
    not_visited_list = {}
    visited = {}
    cur_path = queue.PriorityQueue()
    mst_weights = get_MST(maze, goals_left, heuristic_list)
    total_l = mst_weights
    s_row, s_col = maze.getStart()
    start_state = ctor(s_row, s_col, 0, total_l)
    start_state.not_visited = maze.getObjectives()
    objectives = maze.getObjectives()

    cur_path.put(start_state)
    not_visited_list[(s_row, s_col)] = len(start_state.not_visited)

    while len(goals_left)>0:
        cur_state = cur_path.get()
        if not cur_state.not_visited:
            break
        for n in cur_state.not_visited:
            n_row, n_col    = n
            n_cost          = cur_state.cost + heuristic_list[(cur_state.position,n)] - 1
            next_state      = ctor(n_row, n_col, n_cost, 0)
            next_state.prev = cur_state
            next_state.level = cur_state.level + 1
            next_state.not_visited = deepcopy(cur_state.not_visited)
            if n in next_state.not_visited:
                next_state.not_visited.remove(n)
            not_visited_list[n] = len(next_state.not_visited)
            if next_state.level > len(start_state.not_visited):
                continue
            mst_weights = get_MST(maze, cur_state.not_visited, heuristic_list)
            next_state.tcost = n_cost + mst_weights
            if len(goals_left) > 1:
                next_state.tcost += len(next_state.not_visited)
            #
            cur_path.put(next_state)
    ret_path = []
    goals_list = []
    while cur_state:
        goals_list.append(cur_state.position)
        cur_state = cur_state.prev
    for i in range(len(goals_list)-1):
        ret_path += edge_list[(goals_list[i] ,goals_list[i+1])][:-1]
    ret_path.append(start)
    ret_path[::-1]
    return ret_path, len(visited)


def get_MST(maze, goals, heuristic_list):
#Prim
    if not len(goals):
        return 0
    start = goals[0]
    visited = {}
    visited[start] = True
    MST_edges = []
    mst_weights = 0
    while len(visited) < len(goals):
        edgequeue = queue.PriorityQueue()
        for v in visited:
            for n in goals:
                if visited.get(n) == True:
                    continue
                new_edge = (v,n)
                new_cost = heuristic_list[new_edge]-1
                edgequeue.put((new_cost,new_edge))
        add_edge = edgequeue.get()
        MST_edges.append(add_edge[1])
        mst_weights += add_edge[0]
        visited[add_edge[1][1]] = True
    return mst_weights

def cost_sofar(start, end, maze):
    cur_path = queue.PriorityQueue()
    visited = {}
    ret_path = []

    start_r, start_c = start
    end_r, end_c = end
    cost = abs(start_r-end_r)+abs(start_c-end_c)
    start_state = ctor(start_r, start_c, 0, cost)

    cur_path.put(start_state)
    visited[(start_r, start_c)] = True
    cur_state = start_state

    while not cur_path.empty():
        cur_state = cur_path.get()
        if cur_state.position == end:
            break
        row1, col1 = cur_state.position
        for n in maze.getNeighbors(row1, col1):
            if visited.get(n) == True:
                continue
            visited[n]     = True
            n_row, n_col    = n
            position        = n
            n_cost          = cur_state.cost + 1
            n_tcost        = n_cost + abs(end[0]-n_row)+abs(end[1]-n_col) # States rated by cost + man_dis
            next_state      = ctor(n_row, n_col, n_cost, n_tcost)
            next_state.prev = cur_state
            cur_path.put(next_state)
    # construct path
    while cur_state:
        ret_path.insert(0, cur_state.position)
        cur_state = cur_state.prev

    return ret_path, len(visited)
#ec astar
# def update_pq(objectives, start):
#     ret = queue.PriorityQueue()
#     for item in objectives:
#         cost = abs(start[0] - item[0]) + abs(start[1] - item[1])
#         ret.put((cost, item))
#     return ret


# def astar(maze):
#     # TODO: Write your code here
#     # return path, num_states_explored
#     cur_pq = queue.PriorityQueue()
#     visited = {}
#     num_states_visited = set()
#     objectives = maze.getObjectives()
#     objectives_pq = update_pq(objectives, maze.getStart())
#     cur_cost, cur_goal = objectives_pq.get()
#     # pq item - tuple: (distance, path list)
#     cur_pq.put((cur_cost, [maze.getStart()]))

#     while not cur_pq.empty():
#         cur_path = cur_pq.get()[1]
#         cur_row, cur_col = cur_path[-1]
#         if (cur_row, cur_col) in visited:
#             continue
#         cur_cost = abs(cur_row - cur_goal[0]) + \
#             abs(cur_col - cur_goal[1]) + len(cur_path) - 1
#         visited[(cur_row, cur_col)] = cur_cost
#         num_states_visited.add((cur_row, cur_col))
#         if (cur_row, cur_col) in objectives:
#             objectives.remove((cur_row, cur_col))
#             if len(objectives) == 0:
#                 return cur_path, len(num_states_visited)
#             else:
#                 objectives_pq = update_pq(objectives, (cur_row, cur_col))
#                 cur_cost, cur_goal = objectives_pq.get()
#                 cur_pq = queue.PriorityQueue()
#                 cur_pq.put((cur_cost, cur_path))
#                 visited.clear()
#                 continue

#         for item in maze.getNeighbors(cur_row, cur_col):
#             new_cost = abs(item[0] - cur_goal[0]) + \
#                 abs(item[1] - cur_goal[1]) + len(cur_path) - 1
#             if item not in visited:
#                 cur_pq.put((new_cost, cur_path + [item]))
#             else:
#                 # if a node that’s already in the explored set found, test to see if the new h(n)+g(n) is smaller than the old one.
#                 if visited[item] > new_cost:
#                     visited[item] = new_cost
#                     cur_pq.put((new_cost, cur_path + [item]))
#     return [], 0
