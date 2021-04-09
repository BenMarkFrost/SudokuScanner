import sys
from copy import deepcopy
from memoization import cached
from func_timeout import func_set_timeout


# @func_set_timeout(2)
@cached(max_size=128, thread_safe=True)
def solveSudoku(sudoku):
    sudoku = read(sudoku)
    return solve(sudoku)

# Non-commented code attributed to https://stackoverflow.com/questions/1697334/algorithm-for-solving-sudoku/35500280

def output(a):
    sys.stdout.write(str(a))

N = 9

def print_field(field):
    if not field:
        output("No solution")
        return
    for i in range(N):
        for j in range(N):
            cell = field[i][j]
            if cell == 0 or isinstance(cell, set):
                output('.')
            else:
                output(cell)
            if (j + 1) % 3 == 0 and j < 8:
                output(' |')

            if j != 8:
                output(' ')
        output('\n')
        if (i + 1) % 3 == 0 and i < 8:
            output("- - - + - - - + - - -\n")

def read(field):
    """ Read field into state (replace 0 with set of possible values) """

    state = deepcopy(field)
    for i in range(N):
        for j in range(N):
            cell = state[i][j]
            if cell == 0:
                state[i][j] = set(range(1,10))

    return state



def done(state):
    """ Are we done? """

    for row in state:
        for cell in row:
            if isinstance(cell, set):
                return False
    return True


def propagate_step(state):
    """
    Propagate one step.

    @return:  A two-tuple that says whether the configuration
              is solvable and whether the propagation changed
              the state.
    """

    new_units = False

    # propagate row rule
    for i in range(N):
        row = state[i]
        values = set([x for x in row if not isinstance(x, set)])
        for j in range(N):
            if isinstance(state[i][j], set):
                state[i][j] -= values
                if len(state[i][j]) == 1:
                    val = state[i][j].pop()
                    state[i][j] = val
                    values.add(val)
                    new_units = True
                elif len(state[i][j]) == 0:
                    return False, None

    # propagate column rule
    for j in range(N):
        column = [state[x][j] for x in range(N)]
        values = set([x for x in column if not isinstance(x, set)])
        for i in range(N):
            if isinstance(state[i][j], set):
                state[i][j] -= values
                if len(state[i][j]) == 1:
                    val = state[i][j].pop()
                    state[i][j] = val
                    values.add(val)
                    new_units = True
                elif len(state[i][j]) == 0:
                    return False, None

    # propagate cell rule
    for x in range(3):
        for y in range(3):
            values = set()
            for i in range(3 * x, 3 * x + 3):
                for j in range(3 * y, 3 * y + 3):
                    cell = state[i][j]
                    if not isinstance(cell, set):
                        values.add(cell)
            for i in range(3 * x, 3 * x + 3):
                for j in range(3 * y, 3 * y + 3):
                    if isinstance(state[i][j], set):
                        state[i][j] -= values
                        if len(state[i][j]) == 1:
                            val = state[i][j].pop()
                            state[i][j] = val
                            values.add(val)
                            new_units = True
                        elif len(state[i][j]) == 0:
                            return False, None

    return True, new_units

def propagate(state):
    """ Propagate until we reach a fixpoint """
    while True:
        solvable, new_unit = propagate_step(state)
        if not solvable:
            return False
        if not new_unit:
            return True



def solve(state):
    """ Solve sudoku """

    solvable = propagate(state)

    if not solvable:
        return None

    if done(state):
        return state

    for i in range(N):
        for j in range(N):
            cell = state[i][j]
            if isinstance(cell, set):
                for value in cell:
                    new_state = deepcopy(state)
                    new_state[i][j] = value
                    solved = solve(new_state)
                    if solved is not None:
                        return solved
                return None

# print_field(solve(state))

# import numpy as np
# from memoization import cached
# from func_timeout import func_set_timeout
# import sys
# from copy import deepcopy

# # Make this object oriented?
# # Everything needs to be local due to concurrency

# @func_set_timeout(2)
# @cached(max_size=128, thread_safe=True)
# def solve(sudoku):

#     # print(np.matrix(sudoku))

#     # sudoku = np.array(sudoku)

#     # solution = solveSudoku(sudoku)

#     state = read(sudoku)

#     print_field(solve(state))

#     print(np.matrix(np.array(sudoku)))

#     # print("Solution: ")
#     # print(solution)

#     return True



# # def calculateSolution(sudoku):

# #     # print(sudoku)
    
# #     # heh = input("Try me")

# #     for y in range(9):
# #         for x in range(9):
# #             if sudoku[y][x] == 0:
# #                 for i in range(1,10):
# #                     # print("trying " + str(i))
# #                     if isValid(sudoku, x, y, i):
# #                         # print(str(i) + " is valid")
# #                         sudoku[y][x] = i
# #                         # print(sudoku)
# #                         tmp = calculateSolution(sudoku)
# #                         if tmp is not None:
# #                             return tmp
# #                         sudoku[y][x] = 0
# #                 # print("Impossible solution, backtracking")
# #                 return
            
# #     return sudoku


# # # def isValid(sudoku, x, y, z):

# # #     if sudoku[y][x] == z:
# # #         # print("Searching for current number")
# # #         return True

# # #     if z in sudoku[y]:
# # #         # print(str(z) + " found in row " + str(y))
# # #         # print(sudoku[y])
# # #         return False
# # #     elif z in sudoku[0:9, x:x+1].flatten():
# # #         # print(str(z) + " found in column " + str(x))
# # #         # print(sudoku[0:9, x:x+1].flatten())
# # #         return False
# # #     else:
# # #         thirdX = 0
# # #         if x < 3:
# # #             thirdX = 1
# # #         elif x < 6:
# # #             thirdX = 4
# # #         else:
# # #             thirdX = 7
        
# # #         thirdY = 0
# # #         if y < 3:
# # #             thirdY = 1
# # #         elif y < 6:
# # #             thirdY = 4
# # #         else:
# # #             thirdY = 7


# # #         if z in sudoku[thirdY-1:thirdY+2, thirdX-1:thirdX+2]:
# # #             # print(str(z) + " found in grid " + str(np.matrix(sudoku[thirdY-1:thirdY+2, thirdX-1:thirdX+2])))
# # #             return False
    
# # #     return True