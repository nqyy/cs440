#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
dominos = [np.array([[i],[i]]) for i in range(1,31)]
triominos = [np.array([[i,0],[i,i]]) for i in range(1,21)]

petnominos = [np.array([[0,1,1],
                   [1,1,0],
                   [0,1,0]]),
        np.array([[2],
                  [2],
                  [2],
                  [2],
                  [2]]),
        np.array([[3,0],
                  [3,0],
                  [3,0],
                  [3,3]]),
        np.array([[0,4],
                  [0,4],
                  [4,4],
                  [4,0]]),
        np.array([[5,5],
                  [5,5],
                  [5,0]]),
        np.array([[6,6,6],
                  [0,6,0],
                  [0,6,0]]),
        np.array([[7,0,7], 
                  [7,7,7]]),
        np.array([[8,0,0], 
                  [8,0,0],
                  [8,8,8]]),
        np.array([[9,0,0],
                  [9,9,0],
                  [0,9,9]]),
        np.array([[0,10,0],
                  [10,10,10],
                  [0,10,0]]),
        np.array([[0,11],
                  [11,11],
                  [0,11],
                  [0,11]]),
        np.array([[12,12,0],
                  [0,12,0],
                  [0,12,12]])]
        
        
board_6x10 = np.ones((6,10))
board_5x12 = np.ones((5,12))
board_3x20 = np.ones((3,20))
empty_chessboard = np.ones((8,8))
empty_chessboard[3][3] = empty_chessboard[3][4] = empty_chessboard[4][3]  = empty_chessboard[4][4] = 0

