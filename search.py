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
            return cur_path, len(cur_path)
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
            return cur_path, len(cur_path)
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
            return cur_path, len(cur_path)
        for item in maze.getNeighbors(cur_row, cur_col):
            if item not in visited:
                cost = abs(item[0] - result_row) + abs(item[1] - result_col)
                pq.put((cost, cur_path + [item]))
    return [], 0


# astar for part 1

# def astar(maze):
#     # TODO: Write your code here
#     # return path, num_states_explored
#     pq = queue.PriorityQueue()
#     visited = {}
#     result_row, result_col = maze.getObjectives()[0]
#     start_row, start_col = maze.getStart()
#     # pq item - tuple: (distance, path list)
#     cost = abs(start_row-result_row) + abs(start_col - result_col)
#     pq.put((cost, [maze.getStart()]))
#     while not pq.empty():
#         cur_path = pq.get()[1]
#         cur_row, cur_col = cur_path[-1]
#         if (cur_row, cur_col) in visited:
#             continue
#         cur_cost = abs(cur_row - result_row) + \
#             abs(cur_col - result_col) + len(cur_path) - 1
#         visited[(cur_row, cur_col)] = cur_cost
#         if maze.isObjective(cur_row, cur_col):
#             return cur_path, len(cur_path)
#         for item in maze.getNeighbors(cur_row, cur_col):
#             new_cost = abs(item[0] - result_row) + \
#                 abs(item[1] - result_col) + len(cur_path) - 1
#             if item not in visited:
#                 pq.put((new_cost, cur_path + [item]))
#             else:
#                 # if a node that’s already in the explored set found, test to see if the new h(n)+g(n) is smaller than the old one.
#                 if visited[item] > new_cost:
#                     visited[item] = new_cost
#                     pq.put((new_cost, cur_path + [item]))
#     return [], 0

#====================================== PART 2 ===============================================
# astar for part 2
def update_pq(objectives, start):
    ret = queue.PriorityQueue()
    for item in objectives:
        cost = abs(start[0] - item[0]) + abs(start[1] - item[1])
        ret.put((cost, item))
    return ret

def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    cur_pq = queue.PriorityQueue()
    visited = {}
    objectives = maze.getObjectives()
    objectives_pq = update_pq(objectives, maze.getStart())
    cur_cost, cur_goal = objectives_pq.get()
    # pq item - tuple: (distance, path list)
    cur_pq.put((cur_cost, [maze.getStart()]))

    while not cur_pq.empty():
        cur_path = cur_pq.get()[1]
        cur_row, cur_col = cur_path[-1]
        if (cur_row, cur_col) in visited:
            continue
        cur_cost = abs(cur_row - cur_goal[0]) + abs(cur_col - cur_goal[1]) + len(cur_path) - 1
        visited[(cur_row, cur_col)] = cur_cost
        if (cur_row, cur_col) in objectives:
            objectives.remove((cur_row, cur_col))
            if len(objectives) == 0:
                return cur_path, len(cur_path)
            else:
                objectives_pq = update_pq(objectives, (cur_row, cur_col))
                cur_cost, cur_goal = objectives_pq.get()
                cur_pq = queue.PriorityQueue()
                cur_pq.put((cur_cost, cur_path))
                visited.clear()
                continue
            
        for item in maze.getNeighbors(cur_row, cur_col):
            new_cost = abs(item[0] - cur_goal[0]) + abs(item[1] - cur_goal[1]) + len(cur_path) - 1
            if item not in visited:
                cur_pq.put((new_cost, cur_path + [item]))
            else:
                # if a node that’s already in the explored set found, test to see if the new h(n)+g(n) is smaller than the old one.
                if visited[item] > new_cost:
                    visited[item] = new_cost
                    cur_pq.put((new_cost, cur_path + [item]))
    return [], 0
