from server import sudokusolver
# from server.Sudoku import Sudoku
from sudoku import Sudoku
import time
import numpy as np
from memoization import cached

# def findNextCellToFill(grid, i, j):
#         for x in range(i,9):
#                 for y in range(j,9):
#                         if grid[x][y] == 0:
#                                 return x,y
#         for x in range(0,9):
#                 for y in range(0,9):
#                         if grid[x][y] == 0:
#                                 return x,y
#         return -1,-1

# def isValid(grid, i, j, e):
#         rowOk = all([e != grid[i][x] for x in range(9)])
#         if rowOk:
#                 columnOk = all([e != grid[x][j] for x in range(9)])
#                 if columnOk:
#                         # finding the top left x,y co-ordinates of the section containing the i,j cell
#                         secTopX, secTopY = 3 *(i//3), 3 *(j//3) #floored quotient should be used here. 
#                         for x in range(secTopX, secTopX+3):
#                                 for y in range(secTopY, secTopY+3):
#                                         if grid[x][y] == e:
#                                                 return False
#                         return True
#         return False

# def solveSudoku(grid, i=0, j=0):
#         i,j = findNextCellToFill(grid, i, j)
#         if i == -1:
#                 return True
#         for e in range(1,10):
#                 if isValid(grid,i,j,e):
#                         grid[i][j] = e
#                         if solveSudoku(grid, i, j):
#                                 return True
#                         # Undo the current cell for backtracking
#                         grid[i][j] = 0
#         return False

# testSudoku1 = [[7, 2, 3, 0, 0, 0, 1, 5, 9], [6, 0, 0, 3, 0, 2, 0, 0, 8], [8, 0, 0, 0, 1, 0, 0, 0, 2], [0, 7, 0, 6, 5, 4, 0, 2, 0], [0, 0, 4, 2, 0, 7, 3, 0, 0], [0, 5, 0, 9, 3, 1, 0, 4, 0], [5, 0, 0, 0, 7, 0, 0, 0, 3], [4, 0, 0, 1, 0, 3, 0, 0, 6], [9, 3, 2, 0, 0, 0, 7, 1, 4]]

# testSudoku2 = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 0, 8, 5], [0, 0, 1, 0, 2, 0, 0, 0, 0], [0, 0, 0, 5, 0, 7, 0, 0, 0], [0, 0, 4, 0, 0, 0, 1, 0, 0], [0, 9, 0, 0, 0, 0, 0, 0, 0], [5, 0, 0, 0, 0, 0, 0, 7, 3], [0, 0, 2, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 4, 0, 0, 0, 9]]

# hardest_sudoku = [
#     [8,0,0,0,0,0,0,0,0],
#     [0,0,3,6,0,0,0,0,0],
#     [0,7,0,0,9,0,2,0,0],
#     [0,5,0,0,0,7,0,0,0],
#     [0,0,0,0,4,5,7,0,0],
#     [0,0,0,1,0,0,0,3,0],
#     [0,0,1,0,0,0,0,6,8],
#     [0,0,8,5,0,0,0,1,0],
#     [0,9,0,0,0,0,4,0,0]]


# @func_set_timeout(2)
@cached(max_size=128, thread_safe=True)
def solve(sudoku):
    start = time.time()

#     print(np.matrix(sudoku))

    puzzle = Sudoku(3,3, board=sudoku)
#     print(puzzle)
    solution = puzzle.solve()

#     print(solution.show())

    stop = time.time()

    print("Solved in:", stop-start, "seconds")

    board = solution.board

    if not puzzle.validate():
        return None

    return board

