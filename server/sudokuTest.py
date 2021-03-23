from server import sudokusolver

testSudoku = [[7, 2, 3, 0, 0, 0, 1, 5, 9], [6, 0, 0, 3, 0, 2, 0, 0, 8], [8, 0, 0, 0, 1, 0, 0, 0, 2], [0, 7, 0, 6, 5, 4, 0, 2, 0], [0, 0, 4, 2, 0, 7, 3, 0, 0], [0, 5, 0, 9, 3, 1, 0, 4, 0], [5, 0, 0, 0, 7, 0, 0, 0, 3], [4, 0, 0, 1, 0, 3, 0, 0, 6], [9, 3, 2, 0, 0, 0, 7, 1, 4]]

solution = sudokusolver.solve(testSudoku)

# print(solution)