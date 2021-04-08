import numpy as np
from memoization import cached
from func_timeout import func_set_timeout

# Make this object oriented?
# Everything needs to be local due to concurrency

@func_set_timeout(0.5)
@cached(max_size=128)
def solve(sudoku):

    # print(np.matrix(sudoku))

    solution = calculateSolution(np.array(sudoku))

    # print("Solution: ")
    # print(solution)

    return solution

def calculateSolution(sudoku):

    # print(sudoku)
    
    # heh = input("Try me")

    for y in range(9):
        for x in range(9):
            if sudoku[y][x] == 0:
                for i in range(1,10):
                    # print("trying " + str(i))
                    if isValid(sudoku, x, y, i):
                        # print(str(i) + " is valid")
                        sudoku[y][x] = i
                        # print(sudoku)
                        tmp = calculateSolution(sudoku)
                        if tmp is not None:
                            return tmp
                        sudoku[y][x] = 0
                # print("Impossible solution, backtracking")
                return
            
    return sudoku


def isValid(sudoku, x, y, z):

    if sudoku[y][x] == z:
        # print("Searching for current number")
        return True

    if z in sudoku[y]:
        # print(str(z) + " found in row " + str(y))
        # print(sudoku[y])
        return False
    elif z in sudoku[0:9, x:x+1].flatten():
        # print(str(z) + " found in column " + str(x))
        # print(sudoku[0:9, x:x+1].flatten())
        return False
    else:
        thirdX = 0
        if x < 3:
            thirdX = 1
        elif x < 6:
            thirdX = 4
        else:
            thirdX = 7
        
        thirdY = 0
        if y < 3:
            thirdY = 1
        elif y < 6:
            thirdY = 4
        else:
            thirdY = 7


        if z in sudoku[thirdY-1:thirdY+2, thirdX-1:thirdX+2]:
            # print(str(z) + " found in grid " + str(np.matrix(sudoku[thirdY-1:thirdY+2, thirdX-1:thirdX+2])))
            return False
    
    return True