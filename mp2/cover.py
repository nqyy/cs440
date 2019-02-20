import numpy as np



# 1. If the matrix A has no columns, the current partial solution
#    is a valid solution; terminate successfully.
# 2. Otherwise, choose a column c (deterministically).
# 3. Choose a row r such that A[r] = 1 (nondeterministically).
# 4. Include row r in the partial solution.
# 5. For each column j such that A[r][j] = 1,
#         for each row i such that A[i][j] = 1,
#             delete row i from matrix A.
#       delete column j from matrix A.
# 6. Repeat this algorithm recursively on the reduced matrix A.



def exact_cover(A,partial):
    # If matrix has no columns, terminate successfully.
    row,col = A.shape
    if col == 0:
        return partial
    else:
        # Choose a column c with the fewest 1s.
        c = A.sum(axis=0).argmin()
        # if column have no 1 in it, it will terminate unsuccessfully
        if A.sum(axis=0)[c] == 0 :
            return None
        # For each row r such that A[r,c] = 1,

        partial_temp = []
        for r in range(row):
            B = A.copy()
            if B[r][c] != 1:
                continue
            partial_temp.append(r)
            # For each column j such that A[r,j] = 1,
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
            B = np.delete(B,col_temp,axis = 1)

            if exact_cover(B,partial_temp) is not None:
                return exact_cover(B,partial_temp)




if __name__ == "__main__":
    x = np.array([[1, 2, 3],
                  [4, 0, 6],
                  [7, 8, 9]])
    t = []
    t.append(0)
    x = np.delete(x, t, axis=1)
    print ( x)
    zzz = np.array([[1,1,0,1]])
    zs = zzz.sum(axis=0).argmin()
    if zzz.sum(axis=0)[zs] == 0 and zs ==2 :
        print("wo gueen!")