from time import sleep
from math import inf
from random import randint
import time


class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board = [['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_'],
                      ['_', '_', '_', '_', '_', '_', '_', '_', '_']]
        self.maxPlayer = 'X'
        self.minPlayer = 'O'
        self.maxDepth = 3
        # The start indexes of each local board
        self.globalIdx = [(0, 0), (0, 3), (0, 6), (3, 0),
                          (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]

        # Start local board index for reflex agent playing
        self.startBoardIdx = 4
        # self.startBoardIdx = randint(0, 8)

        # utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility = 10000
        self.twoInARowMaxUtility = 500
        self.preventThreeInARowMaxUtility = 100
        self.cornerMaxUtility = 30

        self.winnerMinUtility = -10000
        self.twoInARowMinUtility = -100
        self.preventThreeInARowMinUtility = -500
        self.cornerMinUtility = -30

        self.expandedNodes = 0
        self.currPlayer = True

    def getNextBoardIdx(self, i, j):
        return (i % 3) * 3 + j % 3

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row])
                         for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row])
                         for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row])
                         for row in self.board[6:9]])+'\n')

    def evaluatePredifined(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        # YOUR CODE HERE
        if self.checkWinner() == 1 and isMax:
            return 10000
        elif self.checkWinner() == -1 and not isMax:
            return -10000

        score = 0

        counter_500 = 0
        counter_100 = 0
        for i in range(9):
            row, col = self.globalIdx[i]

            cur_player = ''
            opponent_player = ''
            if isMax:
                cur_player = self.maxPlayer
                opponent_player = self.minPlayer
            else:
                cur_player = self.minPlayer
                opponent_player = self.maxPlayer
            # 500
            # ROW
            if self.board[row][col] == self.board[row][col+1] == cur_player and self.board[row][col+2] == '_':
                counter_500 += 1
            elif self.board[row][col+1] == self.board[row][col+2] == cur_player and self.board[row][col] == '_':
                counter_500 += 1
            elif self.board[row][col] == self.board[row][col+2] == cur_player and self.board[row][col+1] == '_':
                counter_500 += 1

            if self.board[row+1][col] == self.board[row+1][col+1] == cur_player and self.board[row+1][col+2] == '_':
                counter_500 += 1
            elif self.board[row+1][col+1] == self.board[row+1][col+2] == cur_player and self.board[row+1][col] == '_':
                counter_500 += 1
            elif self.board[row+1][col] == self.board[row+1][col+2] == cur_player and self.board[row+1][col+1] == '_':
                counter_500 += 1

            if self.board[row+2][col] == self.board[row+2][col+1] == cur_player and self.board[row+2][col+2] == '_':
                counter_500 += 1
            elif self.board[row+2][col+1] == self.board[row+2][col+2] == cur_player and self.board[row+2][col] == '_':
                counter_500 += 1
            elif self.board[row+2][col] == self.board[row+2][col+2] == cur_player and self.board[row+2][col+1] == '_':
                counter_500 += 1
            # COL
            if self.board[row][col] == self.board[row+1][col] == cur_player and self.board[row+2][col] == '_':
                counter_500 += 1
            elif self.board[row+1][col] == self.board[row+2][col] == cur_player and self.board[row][col] == '_':
                counter_500 += 1
            elif self.board[row][col] == self.board[row+2][col] == cur_player and self.board[row+1][col] == '_':
                counter_500 += 1

            if self.board[row][col+1] == self.board[row+1][col+1] == cur_player and self.board[row+2][col+1] == '_':
                counter_500 += 1
            elif self.board[row+1][col+1] == self.board[row+2][col+1] == cur_player and self.board[row][col+1] == '_':
                counter_500 += 1
            elif self.board[row][col+1] == self.board[row+2][col+1] == cur_player and self.board[row+1][col+1] == '_':
                counter_500 += 1

            if self.board[row][col+2] == self.board[row+1][col+2] == cur_player and self.board[row+2][col+2] == '_':
                counter_500 += 1
            elif self.board[row+1][col+2] == self.board[row+2][col+2] == cur_player and self.board[row][col+2] == '_':
                counter_500 += 1
            elif self.board[row][col+2] == self.board[row+2][col+2] == cur_player and self.board[row+1][col+2] == '_':
                counter_500 += 1
            # DIA
            if self.board[row][col] == self.board[row+1][col+1] == cur_player and self.board[row+2][col+2] == '_':
                counter_500 += 1
            elif self.board[row+2][col+2] == self.board[row+1][col+1] == cur_player and self.board[row][col] == '_':
                counter_500 += 1
            elif self.board[row+2][col+2] == self.board[row][col] == cur_player and self.board[row+1][col+1] == '_':
                counter_500 += 1

            if self.board[row][col+2] == self.board[row+1][col+1] == cur_player and self.board[row+2][col] == '_':
                counter_500 += 1
            elif self.board[row][col+2] == self.board[row+2][col] == cur_player and self.board[row+1][col+1] == '_':
                counter_500 += 1
            elif self.board[row+1][col+1] == self.board[row+2][col] == cur_player and self.board[row][col+2] == '_':
                counter_500 += 1
            # 100
            # ROW
            if self.board[row][col] == self.board[row][col+1] == opponent_player and self.board[row][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row][col+1] == self.board[row][col+2] == opponent_player and self.board[row][col] == cur_player:
                counter_100 += 1
            elif self.board[row][col] == self.board[row][col+2] == opponent_player and self.board[row][col+1] == cur_player:
                counter_100 += 1

            if self.board[row+1][col] == self.board[row+1][col+1] == opponent_player and self.board[row+1][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col+1] == self.board[row+1][col+2] == opponent_player and self.board[row+1][col] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col] == self.board[row+1][col+2] == opponent_player and self.board[row+1][col+1] == cur_player:
                counter_100 += 1

            if self.board[row+2][col] == self.board[row+2][col+1] == opponent_player and self.board[row+2][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row+2][col+1] == self.board[row+2][col+2] == opponent_player and self.board[row+2][col] == cur_player:
                counter_100 += 1
            elif self.board[row+2][col] == self.board[row+2][col+2] == opponent_player and self.board[row+2][col+1] == cur_player:
                counter_100 += 1

            # COL
            if self.board[row][col] == self.board[row+1][col] == opponent_player and self.board[row+2][col] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col] == self.board[row+2][col] == opponent_player and self.board[row][col] == cur_player:
                counter_100 += 1
            elif self.board[row][col] == self.board[row+2][col] == opponent_player and self.board[row+1][col] == cur_player:
                counter_100 += 1

            if self.board[row][col+1] == self.board[row+1][col+1] == opponent_player and self.board[row+2][col+1] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col+1] == self.board[row+2][col+1] == opponent_player and self.board[row][col+1] == cur_player:
                counter_100 += 1
            elif self.board[row][col+1] == self.board[row+2][col+1] == opponent_player and self.board[row+1][col+1] == cur_player:
                counter_100 += 1

            if self.board[row][col+2] == self.board[row+1][col+2] == opponent_player and self.board[row+2][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col+2] == self.board[row+2][col+2] == opponent_player and self.board[row][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row][col+2] == self.board[row+2][col+2] == opponent_player and self.board[row+1][col+2] == cur_player:
                counter_100 += 1
            # DIA
            if self.board[row][col] == self.board[row+1][col+1] == opponent_player and self.board[row+2][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row+2][col+2] == self.board[row+1][col+1] == opponent_player and self.board[row][col] == cur_player:
                counter_100 += 1
            elif self.board[row+2][col+2] == self.board[row][col] == opponent_player and self.board[row+1][col+1] == cur_player:
                counter_100 += 1

            if self.board[row][col+2] == self.board[row+1][col+1] == opponent_player and self.board[row+2][col] == cur_player:
                counter_100 += 1
            elif self.board[row][col+2] == self.board[row+2][col] == opponent_player and self.board[row+1][col+1] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col+1] == self.board[row+2][col] == opponent_player and self.board[row][col+2] == cur_player:
                counter_100 += 1

        if isMax:
            score = score + 500 * counter_500 + 100 * counter_100
        else:
            score = score - (100 * counter_500 + 500 * counter_100)

        if score == 0:
            for i in range(9):
                row, col = self.globalIdx[i]
                for y, x in [(row, col), (row+2, col), (row, col+2), (row+2, col+2)]:
                    if self.board[y][x] == self.maxPlayer and isMax:
                        score += 30
                    elif self.board[y][x] == self.minPlayer and not isMax:
                        score -= 30
        return score

    def evaluateDesigned(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        # YOUR CODE HERE
        if self.checkWinner() == 1:
            return 10000
        elif self.checkWinner() == -1:
            return -10000

        score = 0

        counter_500 = 0
        counter_100 = 0
        for i in range(9):
            row, col = self.globalIdx[i]

            cur_player = ''
            opponent_player = ''
            if isMax:
                cur_player = self.maxPlayer
                opponent_player = self.minPlayer
            else:
                cur_player = self.minPlayer
                opponent_player = self.maxPlayer
            # 500
            # ROW
            if self.board[row][col] == self.board[row][col+1] == cur_player and self.board[row][col+2] == '_':
                counter_500 += 1
            elif self.board[row][col+1] == self.board[row][col+2] == cur_player and self.board[row][col] == '_':
                counter_500 += 1
            elif self.board[row][col] == self.board[row][col+2] == cur_player and self.board[row][col+1] == '_':
                counter_500 += 1

            if self.board[row+1][col] == self.board[row+1][col+1] == cur_player and self.board[row+1][col+2] == '_':
                counter_500 += 1
            elif self.board[row+1][col+1] == self.board[row+1][col+2] == cur_player and self.board[row+1][col] == '_':
                counter_500 += 1
            elif self.board[row+1][col] == self.board[row+1][col+2] == cur_player and self.board[row+1][col+1] == '_':
                counter_500 += 1

            if self.board[row+2][col] == self.board[row+2][col+1] == cur_player and self.board[row+2][col+2] == '_':
                counter_500 += 1
            elif self.board[row+2][col+1] == self.board[row+2][col+2] == cur_player and self.board[row+2][col] == '_':
                counter_500 += 1
            elif self.board[row+2][col] == self.board[row+2][col+2] == cur_player and self.board[row+2][col+1] == '_':
                counter_500 += 1
            # COL
            if self.board[row][col] == self.board[row+1][col] == cur_player and self.board[row+2][col] == '_':
                counter_500 += 1
            elif self.board[row+1][col] == self.board[row+2][col] == cur_player and self.board[row][col] == '_':
                counter_500 += 1
            elif self.board[row][col] == self.board[row+2][col] == cur_player and self.board[row+1][col] == '_':
                counter_500 += 1

            if self.board[row][col+1] == self.board[row+1][col+1] == cur_player and self.board[row+2][col+1] == '_':
                counter_500 += 1
            elif self.board[row+1][col+1] == self.board[row+2][col+1] == cur_player and self.board[row][col+1] == '_':
                counter_500 += 1
            elif self.board[row][col+1] == self.board[row+2][col+1] == cur_player and self.board[row+1][col+1] == '_':
                counter_500 += 1

            if self.board[row][col+2] == self.board[row+1][col+2] == cur_player and self.board[row+2][col+2] == '_':
                counter_500 += 1
            elif self.board[row+1][col+2] == self.board[row+2][col+2] == cur_player and self.board[row][col+2] == '_':
                counter_500 += 1
            elif self.board[row][col+2] == self.board[row+2][col+2] == cur_player and self.board[row+1][col+2] == '_':
                counter_500 += 1
            # DIA
            if self.board[row][col] == self.board[row+1][col+1] == cur_player and self.board[row+2][col+2] == '_':
                counter_500 += 1
            elif self.board[row+2][col+2] == self.board[row+1][col+1] == cur_player and self.board[row][col] == '_':
                counter_500 += 1
            elif self.board[row+2][col+2] == self.board[row][col] == cur_player and self.board[row+1][col+1] == '_':
                counter_500 += 1

            if self.board[row][col+2] == self.board[row+1][col+1] == cur_player and self.board[row+2][col] == '_':
                counter_500 += 1
            elif self.board[row][col+2] == self.board[row+2][col] == cur_player and self.board[row+1][col+1] == '_':
                counter_500 += 1
            elif self.board[row+1][col+1] == self.board[row+2][col] == cur_player and self.board[row][col+2] == '_':
                counter_500 += 1
            # 100
            # ROW
            if self.board[row][col] == self.board[row][col+1] == opponent_player and self.board[row][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row][col+1] == self.board[row][col+2] == opponent_player and self.board[row][col] == cur_player:
                counter_100 += 1
            elif self.board[row][col] == self.board[row][col+2] == opponent_player and self.board[row][col+1] == cur_player:
                counter_100 += 1

            if self.board[row+1][col] == self.board[row+1][col+1] == opponent_player and self.board[row+1][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col+1] == self.board[row+1][col+2] == opponent_player and self.board[row+1][col] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col] == self.board[row+1][col+2] == opponent_player and self.board[row+1][col+1] == cur_player:
                counter_100 += 1

            if self.board[row+2][col] == self.board[row+2][col+1] == opponent_player and self.board[row+2][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row+2][col+1] == self.board[row+2][col+2] == opponent_player and self.board[row+2][col] == cur_player:
                counter_100 += 1
            elif self.board[row+2][col] == self.board[row+2][col+2] == opponent_player and self.board[row+2][col+1] == cur_player:
                counter_100 += 1

            # COL
            if self.board[row][col] == self.board[row+1][col] == opponent_player and self.board[row+2][col] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col] == self.board[row+2][col] == opponent_player and self.board[row][col] == cur_player:
                counter_100 += 1
            elif self.board[row][col] == self.board[row+2][col] == opponent_player and self.board[row+1][col] == cur_player:
                counter_100 += 1

            if self.board[row][col+1] == self.board[row+1][col+1] == opponent_player and self.board[row+2][col+1] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col+1] == self.board[row+2][col+1] == opponent_player and self.board[row][col+1] == cur_player:
                counter_100 += 1
            elif self.board[row][col+1] == self.board[row+2][col+1] == opponent_player and self.board[row+1][col+1] == cur_player:
                counter_100 += 1

            if self.board[row][col+2] == self.board[row+1][col+2] == opponent_player and self.board[row+2][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col+2] == self.board[row+2][col+2] == opponent_player and self.board[row][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row][col+2] == self.board[row+2][col+2] == opponent_player and self.board[row+1][col+2] == cur_player:
                counter_100 += 1
            # DIA
            if self.board[row][col] == self.board[row+1][col+1] == opponent_player and self.board[row+2][col+2] == cur_player:
                counter_100 += 1
            elif self.board[row+2][col+2] == self.board[row+1][col+1] == opponent_player and self.board[row][col] == cur_player:
                counter_100 += 1
            elif self.board[row+2][col+2] == self.board[row][col] == opponent_player and self.board[row+1][col+1] == cur_player:
                counter_100 += 1

            if self.board[row][col+2] == self.board[row+1][col+1] == opponent_player and self.board[row+2][col] == cur_player:
                counter_100 += 1
            elif self.board[row][col+2] == self.board[row+2][col] == opponent_player and self.board[row+1][col+1] == cur_player:
                counter_100 += 1
            elif self.board[row+1][col+1] == self.board[row+2][col] == opponent_player and self.board[row][col+2] == cur_player:
                counter_100 += 1

        if isMax:
            score = score + 500 * counter_500 + 100 * counter_100
        else:
            score = score - (100 * counter_500 + 500 * counter_100)

        for i in range(9):
            row, col = self.globalIdx[i]
            for y, x in [(row, col), (row+2, col), (row, col+2), (row+2, col+2)]:
                if self.board[y][x] == self.maxPlayer:
                    score += 30
                elif self.board[y][x] == self.minPlayer:
                    score -= 30
        return score

    def checkMovesLeft(self):
        """
        This function checks whether any legal move remains on the board.
        output:
        movesLeft(bool): boolean variable indicates whether any legal move remains
                        on the board.
        """
        # YOUR CODE HERE
        movesLeft = False
        if any('_' in sublist for sublist in self.board):
            movesLeft = True
        return movesLeft

    def checkWinner(self):
        # Return termimnal node status for maximizer player 1-win,0-tie,-1-lose
        """
        This function checks whether there is a winner on the board.
        output:
        winner(int): Return 0 if there is no winner.
                     Return 1 if maxPlayer is the winner.
                     Return -1 if miniPlayer is the winner.
        """
        # YOUR CODE HERE
        win_symbol = ''
        for i in range(9):
            row, col = self.globalIdx[i]
            if self.board[row][col] == self.board[row+1][col] == self.board[row+2][col] != '_':
                win_symbol = self.board[row][col]
            elif self.board[row][col+1] == self.board[row+1][col+1] == self.board[row+2][col+1] != '_':
                win_symbol = self.board[row][col+1]
            elif self.board[row][col+2] == self.board[row+1][col+2] == self.board[row+2][col+2] != '_':
                win_symbol = self.board[row][col+2]
            elif self.board[row][col] == self.board[row][col+1] == self.board[row][col+2] != '_':
                win_symbol = self.board[row][col]
            elif self.board[row+1][col] == self.board[row+1][col+1] == self.board[row+1][col+2] != '_':
                win_symbol = self.board[row+1][col]
            elif self.board[row+2][col] == self.board[row+2][col+1] == self.board[row+2][col+2] != '_':
                win_symbol = self.board[row+2][col]
            elif self.board[row][col] == self.board[row+1][col+1] == self.board[row+2][col+2] != '_':
                win_symbol = self.board[row][col]
            elif self.board[row][col+2] == self.board[row+1][col+1] == self.board[row+2][col] != '_':
                win_symbol = self.board[row][col+2]
            if win_symbol == 'X':
                return 1
            elif win_symbol == 'O':
                return -1
        return 0

    def alphabeta(self, depth, currBoardIdx, alpha, beta, isMax):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        best_value(float):the best_value that current player may have
        """
        # YOUR CODE HERE
        if (depth == self.maxDepth) or (not self.checkMovesLeft()) or (self.checkWinner() != 0):
            self.expandedNodes += 1
            return self.evaluatePredifined(self.currPlayer)

        if isMax:
            # max from child
            best_value = -inf
            y, x = self.globalIdx[currBoardIdx]
            for j in range(3):
                for i in range(3):
                    if self.board[y+j][x+i] == '_':
                        self.board[y+j][x+i] = self.maxPlayer
                        cur_value = self.alphabeta(depth+1, self.getNextBoardIdx(y+j, x+i), alpha, beta, not isMax)
                        self.board[y+j][x+i] = '_'
                        best_value = max(best_value, cur_value)
                        alpha = max(alpha, best_value)
                        if beta <= alpha:
                            return best_value
            return best_value
        else:
            # min from child
            best_value = inf
            y, x = self.globalIdx[currBoardIdx]
            for j in range(3):
                for i in range(3):
                    if self.board[y+j][x+i] == '_':
                        self.board[y+j][x+i] = self.minPlayer
                        cur_value = self.alphabeta(depth+1, self.getNextBoardIdx(y+j, x+i), alpha, beta, not isMax)
                        self.board[y+j][x+i] = '_'
                        best_value = min(best_value, cur_value)
                        beta = min(beta, best_value)
                        if beta <= alpha:
                            return best_value
            return best_value

    def minimax(self, depth, currBoardIdx, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        # YOUR CODE HERE
        if (depth == self.maxDepth) or (not self.checkMovesLeft()) or (self.checkWinner() != 0):
            self.expandedNodes += 1
            return self.evaluatePredifined(self.currPlayer)

        if isMax:
            # max from child
            best_value = -inf
            y, x = self.globalIdx[currBoardIdx]
            for j in range(3):
                for i in range(3):
                    if self.board[y+j][x+i] == '_':
                        self.board[y+j][x+i] = self.maxPlayer
                        cur_value = self.minimax(depth+1, self.getNextBoardIdx(y+j, x+i), not isMax)
                        self.board[y+j][x+i] = '_'
                        best_value = max(best_value, cur_value)
            return best_value
        else:
            # min from child
            best_value = inf
            y, x = self.globalIdx[currBoardIdx]
            for j in range(3):
                for i in range(3):
                    if self.board[y+j][x+i] == '_':
                        self.board[y+j][x+i] = self.minPlayer
                        cur_value = self.minimax(depth+1, self.getNextBoardIdx(y+j, x+i), not isMax)
                        self.board[y+j][x+i] = '_'
                        best_value = min(best_value, cur_value)
            return best_value

    def playGamePredifinedAgent(self, maxFirst, isMinimaxOffensive, isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        # YOUR CODE HERE
        cur_player = maxFirst
        cur_board = self.startBoardIdx
        self.expandedNodes = 0
        bestMove = []
        bestValue = []
        gameBoards = []
        expandedNodes = []

        alpha = -inf
        beta = inf
        while self.checkMovesLeft() and self.checkWinner() == 0:
            if cur_player:
                self.currPlayer = True
                y, x = self.globalIdx[cur_board]
                best_coord = (-1, -1)
                best_value = -inf
                for j in range(3):
                    for i in range(3):
                        if self.board[y+j][x+i] == '_':
                            self.board[y+j][x+i] = self.maxPlayer
                            cur_board = self.getNextBoardIdx(y+j, x+i)
                            if isMinimaxOffensive:
                                cur_value = self.minimax(1, cur_board, not cur_player)
                            else:
                                cur_value = self.alphabeta(1, cur_board, alpha, beta, not cur_player)
                            self.board[y+j][x+i] = '_'
                            if cur_value > best_value:
                                best_coord = (y+j, x+i)
                                best_value = cur_value
                self.board[best_coord[0]][best_coord[1]] = self.maxPlayer
                cur_board = self.getNextBoardIdx(best_coord[0], best_coord[1])
                bestMove.append(best_coord)
                bestValue.append(best_value)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                cur_player = not cur_player
            else:
                self.currPlayer = False
                y, x = self.globalIdx[cur_board]
                best_coord = (-1, -1)
                best_value = inf
                for j in range(3):
                    for i in range(3):
                        if self.board[y+j][x+i] == '_':
                            self.board[y+j][x+i] = self.minPlayer
                            cur_board = self.getNextBoardIdx(y+j, x+i)
                            if isMinimaxDefensive:
                                cur_value = self.minimax(1, cur_board, not cur_player)
                            else:
                                cur_value = self.alphabeta(1, cur_board, alpha, beta, not cur_player)
                            self.board[y+j][x+i] = '_'
                            if cur_value < best_value:
                                best_coord = (y+j, x+i)
                                best_value = cur_value
                self.board[best_coord[0]][best_coord[1]] = self.minPlayer
                cur_board = self.getNextBoardIdx(best_coord[0], best_coord[1])
                bestMove.append(best_coord)
                bestValue.append(best_value)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                cur_player = not cur_player

        winner = self.checkWinner()
        return gameBoards, bestMove, expandedNodes, bestValue, winner

    def my_minimax(self, depth, currBoardIdx, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        # YOUR CODE HERE
        if (depth == self.maxDepth) or (not self.checkMovesLeft()) or (self.checkWinner() != 0):
            self.expandedNodes += 1
            return self.evaluateDesigned(self.currPlayer)

        if isMax:
            # max from child
            best_value = -inf
            y, x = self.globalIdx[currBoardIdx]
            for j in range(3):
                for i in range(3):
                    if self.board[y+j][x+i] == '_':
                        self.board[y+j][x+i] = self.maxPlayer
                        cur_value = self.my_minimax(depth+1, self.getNextBoardIdx(y+j, x+i), not isMax)
                        self.board[y+j][x+i] = '_'
                        best_value = max(best_value, cur_value)
            return best_value
        else:
            # min from child
            best_value = inf
            y, x = self.globalIdx[currBoardIdx]
            for j in range(3):
                for i in range(3):
                    if self.board[y+j][x+i] == '_':
                        self.board[y+j][x+i] = self.minPlayer
                        cur_value = self.my_minimax(depth+1, self.getNextBoardIdx(y+j, x+i), not isMax)
                        self.board[y+j][x+i] = '_'
                        best_value = min(best_value, cur_value)
            return best_value

    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        best_coord(list of tuple): list of best_coord coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        # YOUR CODE HERE
        cur_player = True  # true max first, false min first
        cur_board = self.startBoardIdx
        self.expandedNodes = 0
        bestMove = []
        bestValue = []
        gameBoards = []
        expandedNodes = []
        alpha = -inf
        beta = inf

        while self.checkMovesLeft() and self.checkWinner() == 0:
            if cur_player:
                self.currPlayer = True
                y, x = self.globalIdx[cur_board]
                best_coord = (-1, -1)
                best_value = -inf
                for j in range(3):
                    for i in range(3):
                        if self.board[y+j][x+i] == '_':
                            self.board[y+j][x+i] = self.maxPlayer
                            cur_board = self.getNextBoardIdx(y+j, x+i)
                            cur_value = self.minimax(1, cur_board, alpha, beta, not cur_player)
                            self.board[y+j][x+i] = '_'
                            if cur_value > best_value:
                                best_coord = (y+j, x+i)
                                best_value = cur_value
                self.board[best_coord[0]][best_coord[1]] = self.maxPlayer
                cur_board = self.getNextBoardIdx(best_coord[0], best_coord[1])
                bestMove.append(best_coord)
                bestValue.append(best_value)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                cur_player = not cur_player
            else:
                self.currPlayer = False
                y, x = self.globalIdx[cur_board]
                best_coord = (-1, -1)
                best_value = inf
                for j in range(3):
                    for i in range(3):
                        if self.board[y+j][x+i] == '_':
                            self.board[y+j][x+i] = self.minPlayer
                            cur_board = self.getNextBoardIdx(y+j, x+i)
                            cur_value = self.my_minimax(1, cur_board, not cur_player)
                            self.board[y+j][x+i] = '_'
                            if cur_value < best_value:
                                best_coord = (y+j, x+i)
                                best_value = cur_value
                self.board[best_coord[0]][best_coord[1]] = self.minPlayer
                cur_board = self.getNextBoardIdx(best_coord[0], best_coord[1])
                bestMove.append(best_coord)
                bestValue.append(best_value)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                cur_player = not cur_player

        winner = self.checkWinner()
        return gameBoards, bestMove, expandedNodes, bestValue, winner

    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        best_coord(list of tuple): list of best_coord coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        # YOUR CODE HERE
        cur_player = True  # true max first, false min first
        cur_board = self.startBoardIdx
        self.expandedNodes = 0
        bestMove = []
        bestValue = []
        gameBoards = []
        expandedNodes = []

        while self.checkMovesLeft() and self.checkWinner() == 0:
            if cur_player:
                self.currPlayer = True
                y, x = self.globalIdx[cur_board]
                best_coord = (-1, -1)
                best_value = -inf
                for j in range(3):
                    for i in range(3):
                        if self.board[y+j][x+i] == '_':
                            self.board[y+j][x+i] = self.maxPlayer
                            cur_board = self.getNextBoardIdx(y+j, x+i)
                            cur_value = self.my_minimax(1, cur_board, not cur_player)
                            self.board[y+j][x+i] = '_'
                            if cur_value > best_value:
                                best_coord = (y+j, x+i)
                                best_value = cur_value
                self.board[best_coord[0]][best_coord[1]] = self.maxPlayer
                cur_board = self.getNextBoardIdx(best_coord[0], best_coord[1])
                bestMove.append(best_coord)
                bestValue.append(best_value)
                gameBoards.append(self.board)
                expandedNodes.append(self.expandedNodes)
                self.printGameBoard()
                cur_player = not cur_player
            else:
                self.currPlayer = False
                y, x = self.globalIdx[cur_board]

                print("put in board:", cur_board)
                x = input('x:')
                y = input('y:')
                put_y = self.globalIdx[cur_board][0] + int(y)
                put_x = self.globalIdx[cur_board][1] + int(x)
                self.board[put_y][put_x] = self.maxPlayer
                cur_board = self.getNextBoardIdx(put_x, put_y)

                self.board[put_y][put_x] = self.minPlayer
                cur_board = self.getNextBoardIdx(put_y, put_x)
                gameBoards.append(self.board)
                self.printGameBoard()
                cur_player = not cur_player

        winner = self.checkWinner()
        return gameBoards, bestMove, expandedNodes, bestValue, winner


if __name__ == "__main__":
    uttt = ultimateTicTacToe()

    start = time.time()
    # gameBoards, best_coord, expandedNodes, best_value, winner = uttt.playGamePredifinedAgent(True, True, True)
    # print(expandedNodes)
    # print(best_value)

    # gameBoards, best_coord, expandedNodes, best_value, winner = uttt.playGameYourAgent()

    gameBoards, best_coord, expandedNodes, best_value, winner = uttt.playGameHuman()

    print("time spent: ", time.time() - start)

    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")
