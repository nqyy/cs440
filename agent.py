# agent.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Rahul Kunji (rahulsk2@illinois.edu) on 01/16/2019

import pygame

# The agent is only used when a human player is used, and is therefore not annotated much
class Agent():
    def __init__(self, pos, maze, blockSizeX, blockSizeY):
        self.row = pos[0]
        self.col = pos[1]
        self.lastRow = None
        self.lastCol = None
        self.needsUpdate = True
        self.color = (255, 0, 0)
        self.maze = maze
        self.blockSizeX = blockSizeX
        self.blockSizeY = blockSizeY

    def update(self):
        if self.needsUpdate:
            self.needsUpdate = False
            position = (int(self.col * self.blockSizeX - self.blockSizeX / 2), int(self.row * self.blockSizeY - self.blockSizeY / 2))
            pygame.display.flip()

    def canMoveRight(self):
        return self.maze.isValidMove(self.row, self.col + 1)

    def canMoveLeft(self):
        return self.maze.isValidMove(self.row, self.col - 1)
        
    def canMoveUp(self):
        return self.maze.isValidMove(self.row - 1, self.col)

    def canMoveDown(self):
        return self.maze.isValidMove(self.row + 1, self.col)

    def moveRight(self):
        if self.canMoveRight():
            self.lastRow = self.row
            self.lastCol = self.col
            self.needsUpdate = True
            self.col += 1
        
    def moveLeft(self):
        if self.canMoveLeft():
            self.lastRow = self.row
            self.lastCol = self.col
            self.needsUpdate = True
            self.col -= 1

    def moveUp(self):
        if self.canMoveUp():
            self.lastRow = self.row
            self.lastCol = self.col
            self.needsUpdate = True
            self.row -= 1

    def moveDown(self):
        if self.canMoveDown():
            self.lastRow = self.row
            self.lastCol = self.col
            self.needsUpdate = True
            self.row += 1



