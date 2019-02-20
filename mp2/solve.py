# -*- coding: utf-8 -*-
import numpy as np
import instances

pent_dict = {"F": instances.petnominos[0],
             "I": instances.petnominos[1],
             "L": instances.petnominos[2],
             "N": instances.petnominos[3],
             "P": instances.petnominos[4],
             "T": instances.petnominos[5],
             "U": instances.petnominos[6],
             "V": instances.petnominos[7],
             "W": instances.petnominos[8],
             "X": instances.petnominos[9],
             "Y": instances.petnominos[10],
             "Z": instances.petnominos[11]}

counter_dict = {"F": 0,
                "I": 1,
                "L": 2,
                "N": 3,
                "P": 4,
                "T": 5,
                "U": 6,
                "V": 7,
                "W": 8,
                "X": 9,
                "Y": 10,
                "Z": 11}


def all_transformation_list(letter):
    ret = []
    cur_block = np.copy(pent_dict[letter])
    if letter == "F" or letter == "L" or letter == "N" or letter == "P" or letter == "Y":
        # 8 ways
        for _ in range(4):
            cur_block = np.rot90(cur_block)
            ret.append(cur_block)
        cur_block = np.flip(cur_block, 0)
        for _ in range(4):
            cur_block = np.rot90(cur_block)
            ret.append(cur_block)
    elif letter == "T" or letter == "U" or letter == "V" or letter == "W":
        # 4 rotations
        for _ in range(4):
            cur_block = np.rot90(cur_block)
            ret.append(cur_block)
    elif letter == "Z":
        # 2 rotation & 2 mirror
        ret.append(cur_block)
        cur_block = np.rot90(cur_block)
        ret.append(cur_block)
        cur_block = np.flip(cur_block, 0)
        ret.append(cur_block)
        cur_block = np.rot90(cur_block)
        ret.append(cur_block)
    elif letter == "I":
        # 2 rotation
        ret.append(cur_block)
        cur_block = np.rot90(cur_block)
        ret.append(cur_block)
    elif letter == "X":
        # just itself
        ret.append(cur_block)
    return ret


def all_positions(board, letter):
    """ Find all positions to place the pentominoes. """
    ret = []
    info = []
    for cur in all_transformation_list(letter):
        rows, cols = cur.shape
        for i in range(board.shape[0] - rows + 1):
            for j in range(board.shape[1] - cols + 1):
                cur_board = np.copy(board)
                fail = 0
                for x in range(rows):
                    if fail == 1:
                        break
                    for y in range(cols):
                        if cur[x][y] != 0 and cur_board[i+x][j+y] == 1:
                            fail = 1
                            break
                        cur_board[i+x][j+y] = cur[x][y]
                if fail == 0:
                    ret.append(cur_board)
                    info.append((cur, i, j))
    return ret, info


def exact_cover(matrix):
    return exact_cover_helper(matrix, [], list(range(matrix.shape[0])))


def exact_cover_helper(A, partial, original_r):
    # If matrix has no columns, terminate successfully.
    row, col = A.shape
    if col == 0:
        return partial
    else:
        c = A.sum(axis=0).argmin()
        if A.sum(axis=0)[c] == 0:
            return None
        partial_temp = partial.copy()
        for r in range(row):
            B = A.copy()
            if B[r][c] != 1:
                continue
            r_index = original_r[r]
            partial_temp.append(r_index)
            col_temp = []
            row_temp = []
            for j in range(col):
                if B[r][j] != 1:
                    continue
                col_temp.append(j)
                for i in range(row):
                    if B[i][j] == 1:
                        if i not in row_temp:
                            row_temp.append(i)
            # Delete each row i such that A[i,j] = 1
            # then delete column j.
            B = np.delete(B, row_temp, axis=0)
            B = np.delete(B, col_temp, axis=1)
            new_index = [x for x in list(range(row)) if x not in row_temp]
            new_r = [original_r[x] for x in new_index]
            if exact_cover_helper(B, partial_temp, new_r) != None:
                return exact_cover_helper(B, partial_temp, new_r)
            partial_temp.remove(r_index)


def solve(board, pents):
    """
    This is the function you will implement. It will take in a numpy array of the board
    as well as a list of n tiles in the form of numpy arrays. The solution returned
    is of the form [(p1, (row1, col1))...(pn,  (rown, coln))]
    where pi is a tile (may be rotated or flipped), and (rowi, coli) is 
    the coordinate of the upper left corner of pi in the board (lowest row and column index 
    that the tile covers).

    -Use np.flip and np.rot90 to manipulate pentominos.

    -You can assume there will always be a solution.
    """
    board = 1 - board
    # print(board)
    flat_board = board.ravel()
    list_to_delete = np.where(flat_board == 1)
    list_to_delete = [x + 12 for x in list_to_delete]

    matrix = []
    info_matrix = []
    for key, _ in pent_dict.items():
        all_pos_list, all_pos_info = all_positions(board, key)
        for item in all_pos_list:
            item = np.append(np.zeros(12), item)
            item = np.delete(item, list_to_delete)
            item[counter_dict[key]] = 1
            matrix.append(item)
        info_matrix.extend(all_pos_info)

    # matrix is the big 2000 * 72 for exact cover algorithm X
    matrix = np.array(matrix)
    # print("matrix row numbers:", len(matrix))

    matrix[matrix > 0] = 1
    result_list = exact_cover(matrix)

    return_val = []
    for i in result_list:
        info = info_matrix[i]
        # print(info)
        return_val.append((info[0], (info[1], info[2])))
    return return_val
