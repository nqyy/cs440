# mp1.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Rahul Kunji (rahulsk2@illinois.edu) on 01/16/2019

"""
This file contains the main application that is run for this MP. It
initializes the pygame context, and handles the interface between the
game and the search algorithm.
"""

import pygame
import sys
import argparse
import time

from pygame.locals import *
from agent import Agent
from maze import Maze
from search import search

class Application:
    def __init__(self, human=True, scale=20, fps=30):
        self.running = True
        self.displaySurface = None
        self.scale = scale
        self.fps = fps
        self.windowTitle = "CS440 MP1: "
        self.__human = human
    
    # Initializes the pygame context and certain properties of the maze
    def initialize(self, filename):
        self.windowTitle += filename

        self.maze = Maze(filename)
        self.gridDim = self.maze.getDimensions()
        
        self.windowHeight = self.gridDim[0] * self.scale
        self.windowWidth = self.gridDim[1] * self.scale

        self.blockSizeX = int(self.windowWidth / self.gridDim[1])
        self.blockSizeY = int(self.windowHeight / self.gridDim[0])

        if self.__human:
            self.agentRadius = min(self.blockSizeX, self.blockSizeY) / 4
            self.agent = Agent(self.maze.getStart(), self.maze, self.blockSizeX, self.blockSizeY)

    # Once the application is initiated, execute is in charge of drawing the game and dealing with the game loop
    def execute(self, filename, searchMethod, save):
        self.initialize(filename)
                    
        if self.maze is None:
            print("No maze created")
            raise SystemExit
            
        if not self.__human:            
            path, statesExplored = search(self.maze, searchMethod)            
        else:
            path, statesExplored = [], 0

        pygame.init()
        self.displaySurface = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)
        self.displaySurface.fill((255, 255, 255))
        pygame.display.flip()
        pygame.display.set_caption(self.windowTitle)

        if self.__human:
            self.drawPlayer()
        else:
            print("Results")
            print("Path Length:", len(path))
            print("States Explored:", statesExplored)
            self.drawPath(path)
            
        self.drawMaze()
        self.drawStart()
        self.drawObjective()

        pygame.display.flip()
        if save is not None:
            pygame.image.save(self.displaySurface, save)
            self.running = False
        
        clock = pygame.time.Clock()

        while self.running:
            pygame.event.pump()            
            keys = pygame.key.get_pressed()            
            clock.tick(self.fps)

            if (keys[K_ESCAPE]):
                    raise SystemExit

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit

            if self.__human:
                if (keys[K_RIGHT]):
                    self.agent.moveRight()

                if (keys[K_LEFT]):
                    self.agent.moveLeft()

                if (keys[K_UP]):
                    self.agent.moveUp()

                if (keys[K_DOWN]):
                    self.agent.moveDown()                        

                self.gameLoop()                


    # The game loop is where everything is drawn to the context. Only called when a human is playing
    def gameLoop(self):
        self.drawObjective()
        self.drawPlayer()
        self.agent.update()
        pygame.display.flip()

    # Implementation of a color scheme for the path taken
    # If Red-Green does not work for you while debugging (for e.g. color blindness),
    # you can edit the start and end colors by picking appropriate (R, G, B) values
    def getColor(self, pathLength, index):
        # start_color = (r0, g0, b0)
        # end_color = (r1, g1, b1)
        # example:
        # start_color = (64, 224, 208)
        # end_color = (139, 0, 139)
        # default:
        start_color = (255, 0, 0)
        end_color = (0, 255, 0)

        r_step = (end_color[0] - start_color[0]) / pathLength
        g_step = (end_color[1] - start_color[1]) / pathLength
        b_step = (end_color[2] - start_color[2]) / pathLength

        red = start_color[0] + index * r_step
        green = start_color[1] + index * g_step
        blue = start_color[2] + index * b_step

        return (red, green, blue)

    # Draws the path (given as a list of (row, col) tuples) to the display context
    def drawPath(self, path):
        for p in range(len(path)):
            color = self.getColor(len(path), p)
            self.drawSquare(path[p][0], path[p][1], color)

    # Simple wrapper for drawing a wall as a rectangle
    def drawWall(self, row, col):
        pygame.draw.rect(self.displaySurface, (0, 0, 0), (col * self.blockSizeX, row * self.blockSizeY, self.blockSizeX, self.blockSizeY), 0)

    # Simple wrapper for drawing a circle
    def drawCircle(self, row, col, color, radius=None):
        if radius is None:
            radius = min(self.blockSizeX, self.blockSizeY) / 4
        pygame.draw.circle(self.displaySurface, color, (int(col * self.blockSizeX + self.blockSizeX / 2), int(row * self.blockSizeY + self.blockSizeY / 2)), int(radius))


    def drawSquare(self, row, col, color):
        pygame.draw.rect(self.displaySurface, color , (col * self.blockSizeX, row * self.blockSizeY, self.blockSizeX, self.blockSizeY), 0)

    # Draws the player to the display context, and draws the path moved (only called if there is a human player)
    def drawPlayer(self):
        if self.agent.lastRow is not None and self.agent.lastCol is not None:
            self.drawCircle(self.agent.lastRow, self.agent.lastCol, (0, 0, 255))
        self.drawCircle(self.agent.row, self.agent.col, self.agent.color)

    # Draws the objectives to the display context
    def drawObjective(self):
        for obj in self.maze.getObjectives():
            self.drawCircle(obj[0], obj[1], (0, 0, 0))

    # Draws start location of path
    def drawStart(self):
        row,col = self.maze.getStart()
        pygame.draw.rect(self.displaySurface, (0,0,255), (col * self.blockSizeX + self.blockSizeX/4, row * self.blockSizeY + self.blockSizeY/4, self.blockSizeX * 0.5, self.blockSizeY * 0.5), 0)

    # Draws the full maze to the display context
    def drawMaze(self):
        for row in range(self.gridDim[0]):
            for col in range(self.gridDim[1]):
                if self.maze.isWall(row, col):
                    self.drawWall(row, col)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='CS440 MP1 Search')
    
    parser.add_argument('filename',
                        help='path to maze file [REQUIRED]')
    parser.add_argument('--method', dest="search", type=str, default = "bfs", 
                        choices = ["bfs", "dfs", "greedy", "astar"],
                        help='search method - default bfs')
    parser.add_argument('--scale', dest="scale", type=int, default = 20,
                        help='scale - default: 20')
    parser.add_argument('--fps', dest="fps", type=int, default = 30,
                        help='fps for the display - default 30')
    parser.add_argument('--human', default = False, action = "store_true",
                        help='flag for human playable - default False')
    parser.add_argument('--save', dest="save", type=str, default = None, 
                        help='save output to image file - default not saved')
    

    args = parser.parse_args()
    app = Application(args.human, args.scale, args.fps)
    app.execute(args.filename, args.search, args.save)
