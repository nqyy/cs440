from time import sleep
from math import inf
from random import randint


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
        # self.startBoardIdx=randint(0,8)

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

        self.coordinate = (-1, -1)  # coordinate to put mark

    def getnextBoardIdx(self, x, y):
        return (y % 3) * 3 + x % 3

    def getCurrBoardIdx(self, i, j):
        if (i >= 0 and i < 3 and j >= 0 and j < 3):
            return 0
        elif (i >= 0 and i < 3 and j >= 3 and j < 6):
            return 1
        elif (i >= 0 and i < 3 and j >= 6 and j < 9):
            return 2
        elif (i >= 3 and i < 6 and j >= 0 and j < 3):
            return 3
        elif (i >= 3 and i < 6 and j >= 3 and j < 6):
            return 4
        elif (i >= 3 and i < 6 and j >= 6 and j < 9):
            return 5
        elif (i >= 6 and i < 9 and j >= 0 and j < 3):
            return 6
        elif (i >= 6 and i < 9 and j >= 3 and j < 6):
            return 7
        elif (i >= 6 and i < 9 and j >= 6 and j < 9):
            return 8

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
        Whowins = self.checkWinner()
        if Whowins and isMax:
            return 10000
        elif Whowins == -1 and isMax == False:
            return -10000
        score = 0
        for i in range(9):
            row, col = self.globalIdx[i]
            counter1 = counter2 = counter3 = counter4 = counter5 = counter6 = counter7 = counter8 = 0
            if self.board[row][col] == 'X':
                counter1 += 1
            elif self.board[row+1][col] == 'X':
                counter1 += 1
            elif self.board[row+2][col] == 'X':
                counter1 += 1
            if counter1 == 2:
                if self.board[row][col] != '_' and self.board[row+1][col] != '_' and self.board[row+2][col] != '_':
                    if isMax == False:
                        score -= 500
                else:
                    if isMax:
                        score += 500

            if self.board[row][col+1] == 'X':
                counter2 += 1
            elif self.board[row+1][col+1] == 'X':
                counter2 += 1
            elif self.board[row+2][col+1] == 'X':
                counter2 += 1
            if counter2 == 2:
                if self.board[row][col+1] != '_' and self.board[row+1][col+1] != '_' and self.board[row+2][col+1] != '_':
                    if isMax == False:
                        score -= 500
                else:
                    if isMax:
                        score += 500

            if self.board[row][col+2] == 'X':
                counter3 += 1
            elif self.board[row+1][col+2] == 'X':
                counter3 += 1
            elif self.board[row+2][col+2] == 'X':
                counter3 += 1
            if counter3 == 2:
                if self.board[row][col+2] != '_' and self.board[row+1][col+2] != '_' and self.board[row+2][col+2] != '_':
                    if isMax == False:
                        score -= 500
                else:
                    if isMax:
                        score += 500

            if self.board[row][col] == 'X':
                counter4 += 1
            elif self.board[row][col+1] == 'X':
                counter4 += 1
            elif self.board[row][col+2] == 'X':
                counter4 += 1
            if counter4 == 2:
                if self.board[row][col] != '_' and self.board[row][col+1] != '_' and self.board[row][col+2] != '_':
                    if isMax == False:
                        score -= 500
                else:
                    if isMax:
                        score += 500

            if self.board[row+1][col] == 'X':
                counter5 += 1
            elif self.board[row+1][col+1] == 'X':
                counter5 += 1
            elif self.board[row+1][col+2] == 'X':
                counter5 += 1
            if counter5 == 2:
                if self.board[row+1][col] != '_' and self.board[row+1][col+1] != '_' and self.board[row+1][col+2] != '_':
                    if isMax == False:
                        score -= 500
                else:
                    if isMax:
                        score += 500

            if self.board[row+2][col] == 'X':
                counter6 += 1
            elif self.board[row+2][col+1] == 'X':
                counter6 += 1
            elif self.board[row+2][col+2] == 'X':
                counter6 += 1
            if counter6 == 2:
                if self.board[row+2][col] != '_' and self.board[row+2][col+1] != '_' and self.board[row+2][col+2] != '_':
                    if isMax == False:
                        score -= 500
                else:
                    if isMax:
                        score += 500

            if self.board[row][col] == 'X':
                counter7 += 1
            elif self.board[row+1][col+1] == 'X':
                counter7 += 1
            elif self.board[row+2][col+2] == 'X':
                counter7 += 1
            if counter7 == 2:
                if self.board[row][col] != '_' and self.board[row+1][col+1] != '_' and self.board[row+2][col+2] != '_':
                    if isMax == False:
                        score -= 500
                else:
                    if isMax:
                        score += 500

            if self.board[row][col+2] == 'X':
                counter8 += 1
            elif self.board[row+1][col+1] == 'X':
                counter8 += 1
            elif self.board[row+2][col] == 'X':
                counter8 += 1
            if counter8 == 2:
                if self.board[row][col+2] != '_' and self.board[row+1][col+1] != '_' and self.board[row+2][col] != '_':
                    if isMax == False:
                        score -= 500
                else:
                    if isMax:
                        score += 500

            counter1 = counter2 = counter3 = counter4 = counter5 = counter6 = counter7 = counter8 = 0
            if self.board[row][col] == 'O':
                counter1 += 1
            elif self.board[row+1][col] == '0':
                counter1 += 1
            elif self.board[row+2][col] == '0':
                counter1 += 1
            if counter1 == 2:
                if self.board[row][col] != '_' and self.board[row+1][col] != '_' and self.board[row+2][col] != '_':
                    if isMax:
                        score += 100
                else:
                    if isMax == False:
                        score -= 100

            if self.board[row][col+1] == '0':
                counter2 += 1
            elif self.board[row+1][col+1] == '0':
                counter2 += 1
            elif self.board[row+2][col+1] == '0':
                counter2 += 1
            if counter2 == 2:
                if self.board[row][col+1] != '_' and self.board[row+1][col+1] != '_' and self.board[row+2][col+1] != '_':
                    if isMax:
                        score += 500
                else:
                    if isMax == False:
                        score -= 100

            if self.board[row][col+2] == '0':
                counter3 += 1
            elif self.board[row+1][col+2] == '0':
                counter3 += 1
            elif self.board[row+2][col+2] == '0':
                counter3 += 1
            if counter3 == 2:
                if self.board[row][col+2] != '_' and self.board[row+1][col+2] != '_' and self.board[row+2][col+2] != '_':
                    if isMax:
                        score += 100
                else:
                    if isMax == False:
                        score -= 100

            if self.board[row][col] == '0':
                counter4 += 1
            elif self.board[row][col+1] == '0':
                counter4 += 1
            elif self.board[row][col+2] == '0':
                counter4 += 1
            if counter4 == 2:
                if self.board[row][col] != '_' and self.board[row][col+1] != '_' and self.board[row][col+2] != '_':
                    if isMax:
                        score += 100
                else:
                    if isMax == False:
                        score -= 100

            if self.board[row+1][col] == '0':
                counter5 += 1
            elif self.board[row+1][col+1] == '0':
                counter5 += 1
            elif self.board[row+1][col+2] == '0':
                counter5 += 1
            if counter5 == 2:
                if self.board[row+1][col] != '_' and self.board[row+1][col+1] != '_' and self.board[row+1][col+2] != '_':
                    if isMax:
                        score += 100
                else:
                    if isMax == False:
                        score -= 100

            if self.board[row+2][col] == '0':
                counter6 += 1
            elif self.board[row+2][col+1] == '0':
                counter6 += 1
            elif self.board[row+2][col+2] == '0':
                counter6 += 1
            if counter6 == 2:
                if self.board[row+2][col] != '_' and self.board[row+2][col+1] != '_' and self.board[row+2][col+2] != '_':
                    if isMax:
                        score += 100
                else:
                    if isMax == False:
                        score -= 100

            if self.board[row][col] == '0':
                counter7 += 1
            elif self.board[row+1][col+1] == '0':
                counter7 += 1
            elif self.board[row+2][col+2] == '0':
                counter7 += 1
            if counter7 == 2:
                if self.board[row][col] != '_' and self.board[row+1][col+1] != '_' and self.board[row+2][col+2] != '_':
                    if isMax:
                        score += 100
                else:
                    if isMax == False:
                        score -= 100

            if self.board[row][col+2] == '0':
                counter8 += 1
            elif self.board[row+1][col+1] == '0':
                counter8 += 1
            elif self.board[row+2][col] == '0':
                counter8 += 1
            if counter8 == 2:
                if self.board[row][col+2] != '_' and self.board[row+1][col+1] != '_' and self.board[row+2][col] != '_':
                    if isMax:
                        score += 100
                else:
                    if isMax == False:
                        score -= 100

        for i in range(9):
            row, col = self.globalIdx[i]
            for x, y in [(row, col), (row+2, col), (row, col+2), (row+2, col+2)]:
                if self.board[x][y] == self.maxPlayer and isMax:
                    score += 30
                elif self.board[x][y] == self.minPlayer and isMax == False:
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
        score = 0
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
        bestValue(float):the bestValue that current player may have
        """
        # YOUR CODE HERE
        if depth > 3 or (self.checkWinner() != 0) or self.checkMovesLeft():
            return self.evaluatePredifined(isMax)

        if isMax:
            bestValue = -5000
            x, y = self.globalIdx[currBoardIdx]
            for i in range(3):
                for j in range(3):
                    if self.board[i + x][j + y] == '_':
                        self.board[i + x][j + y] = self.maxPlayer
                        self.expandedNodes += 1
                        self.startBoardIdx = self.getnextBoardIdx(i+x, j+y)
                        curValue = self.alphabeta(
                            depth + 1, self.startBoardIdx, alpha, beta, not isMax)
                        if curValue > bestValue:
                            self.coordinate = (i+x, j+y)
                        bestValue = max(bestValue, curValue)
                        self.board[i + x][j + y] = '_'
                        alpha = max(alpha, bestValue)
                        if beta <= alpha:
                            break
            return bestValue

        else:
            bestValue = 5000
            x, y = self.globalIdx[currBoardIdx]
            for i in range(3):
                for j in range(3):
                    if self.board[i + x][j + y] == '_':
                        self.board[i + x][j + y] = self.minPlayer
                        self.expandedNodes += 1
                        self.startBoardIdx = self.getnextBoardIdx(i+x, j+y)
                        curValue = self.alphabeta(
                            depth + 1, self.startBoardIdx, alpha, beta, not isMax)
                        if curValue < bestValue:
                            self.coordinate = (i+x, j+y)
                        bestValue = min(bestValue, curValue)
                        self.board[i + x][j + y] = '_'
                        alpha = min(alpha, bestValue)
                        if beta <= alpha:
                            break
            return bestValue

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
        if depth > self.maxDepth or (self.checkWinner() != 0) or self.checkMovesLeft():
            return self.evaluatePredifined(isMax)

        if isMax:
            bestValue = -5000
            x, y = self.globalIdx[currBoardIdx]
            for i in range(3):
                for j in range(3):
                    if self.board[i + x][j + y] == '_':
                        self.board[i + x][j + y] = self.maxPlayer
                        self.expandedNodes += 1
                        self.startBoardIdx = self.getnextBoardIdx(i+x, j+y)
                        curValue = self.minimax(
                            depth + 1, self.startBoardIdx, not isMax)
                        if curValue > bestValue:
                            self.coordinate = (i+x, j+y)
                        bestValue = max(bestValue, curValue)
                        self.board[i + x][j + y] = '_'
            return bestValue
        else:
            bestValue = 5000
            x, y = self.globalIdx[currBoardIdx]
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.board[i + x][j + y] == '_':
                        self.board[i + x][j + y] = self.minPlayer
                        self.expandedNodes += 1
                        self.startBoardIdx = self.getnextBoardIdx(i+x, j+y)
                        curValue = self.minimax(
                            depth + 1, self.startBoardIdx, not isMax)
                        if curValue < bestValue:
                            self.coordinate = (i+x, j+y)
                        bestValue = min(bestValue, curValue)
                        self.board[i + x][j + y] = '_'
            return bestValue

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
        bestMove = []
        bestValue = []
        gameBoards = []
        expandedNodes = []
        winner = 0

        alpha = 0  # to be assigned
        beta = 0  # to be assigned
        while self.checkMovesLeft():
            # winner check
            winner = self.checkWinner()
            if winner != 0:
                break
            # do the stuff
            if maxFirst:
                for count in range(2):
                    if count == 0:  # max player (offensive player)
                        if isMinimaxOffensive:
                            best_val = self.minimax(
                                1, self.startBoardIdx, True)
                        else:
                            best_val = self.alphabeta(
                                1, self.startBoardIdx, alpha, beta, True)
                        self.board[self.coordinate[0]
                                   ][self.coordinate[1]] = self.maxPlayer
                    else:  # min player (defenseive player)
                        if isMinimaxDefensive:
                            best_val = self.minimax(
                                1, self.startBoardIdx, False)
                        else:
                            best_val = self.alphabeta(
                                1, self.startBoardIdx, alpha, beta, False)
                    bestMove.append(self.coordinate)
                    bestValue.append(best_val)
                    gameBoards.append(self.board)
                    expandedNodes.append(self.expandedNodes)
            else:
                for count in range(2):
                    if count == 1:  # max player (offensive player)
                        if isMinimaxOffensive:
                            best_val = self.minimax(
                                1, self.startBoardIdx, True)
                        else:
                            best_val = self.alphabeta(
                                1, self.startBoardIdx, alpha, beta, True)
                        self.board[self.coordinate[0]
                                   ][self.coordinate[1]] = self.maxPlayer
                    else:  # min player (defenseive player)
                        if isMinimaxDefensive:
                            best_val = self.minimax(
                                1, self.startBoardIdx, False)
                        else:
                            best_val = self.alphabeta(
                                1, self.startBoardIdx, alpha, beta, False)
                    bestMove.append(self.coordinate)
                    bestValue.append(best_val)
                    gameBoards.append(self.board)
                    expandedNodes.append(self.expandedNodes)

        return gameBoards, bestMove, expandedNodes, bestValue, winner

    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        # YOUR CODE HERE
        bestMove = []
        gameBoards = []
        winner = 0
        return gameBoards, bestMove, winner

    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        # YOUR CODE HERE
        bestMove = []
        gameBoards = []
        winner = 0
        return gameBoards, bestMove, winner


if __name__ == "__main__":
    uttt = ultimateTicTacToe()

    gameBoards, bestMove, expandedNodes, bestValue, winner = uttt.playGamePredifinedAgent(
        True, True, True)

    print(gameBoards)

    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")
