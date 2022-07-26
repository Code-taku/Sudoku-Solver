# packages
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy as np
import keyboard
import pyautogui

def solve_sudoku(board):
    '''
    O: empty squares
    1-9: sudoku numbers
    The Sudoku Grid is 0-indexed so 1 has index of 0, 2 has index of 1, etc.
    '''
    
    # Sudoku Board
    # A 2D array where each grid has 9 Boolean Slots to indicate which numbers
    # are valid in that spot, the algorithm will only insert legal numbers when checking

    ROW = [[True for _ in range(9)] for _ in range(9)] # rows
    COL = [[True for _ in range(9)] for _ in range(9)] # columns
    BLK = [[True for _ in range(9)] for _ in range(9)] # 3x3 blocks

    # To compute which 3x3 block a (r, c) coordinate belongs to, we use the formula (r // 3) * 3 + (c // 3) 
    # This gives us the index of the corresponding block (see index reference below)
    # -------------
    # | 0 | 1 | 2 |     ex: coord(4, 0) belongs in block 3 becuase (4 // 3) * 3 + (0 // 3) = 3 
    # |-----------|
    # | 3 | 4 | 5 |
    # |-----------|
    # | 6 | 7 | 8 |
    # -------------

    # list of tuples (r, c) which denote the coordinates on the grid where we need to fill
    missing = []

    # Iterate through Sudoku grid to determine which values are missing and limit
    # the number of legal moves we have
    for r in range(9):
        for c in range(9):
            # 0 means that the grid is empty, so if not empty
            if board[r][c] != 0:
                # mark the row/col/block as False for the number at grid (r, c)
                n = board[r][c] - 1  # adjust for 0-indexed array
                ROW[r][n] = COL[c][n] = BLK[(r // 3) * 3 + (c // 3)][n] = False
            # else the number at current (r, c) is missing so add to our list this coordinate
            else:
                missing.append((r, c))

    # Check for valid combinations by using backtracking
    def backtrack():
        # if we filled in all the missing numbers - Solved! 
        if not missing:
            return True
        
        # Get next missing number
        r, c = missing.pop()

        # for numbers 1-9 (in boolean array indexed 0-8)
        for n in range(9):
            # Check to see if num can be legally added (no duplicate number in ROW, COL and BLK)
            if ROW[r][n] and COL[c][n] and BLK[(r // 3) * 3 + (c // 3)][n]:
                board[r][c] = n + 1 # adjust actual number from index value
                # mark that we are no longer missing a number at this position for the time being
                ROW[r][n] = COL[c][n] = BLK[(r // 3) * 3 + (c // 3)][n] = False

                # recursively call function to check next missing spot until solved
                if backtrack():
                    # found correct combination
                    return True
                
                # Else backtracking failed so rest value at position (r, c) and try another number
                board[r][c] = 0
                ROW[r][n] = COL[c][n] = BLK[(r // 3) * 3 + (c // 3)][n] = True
            
        # After checking 1-9, found no legal moves for position (r, c), this indicates that the 
        # previous choices we made were wrong so must backtrack further
        missing.append((r, c))
        return False

    backtrack()

# sample hard puzzle taken from Sudoku Research Page of Timo and Janne - University of Vaasa:
# puzzle = [
#     [0, 0, 0, 0, 0, 3, 0, 1, 7],
#     [0, 1, 5, 0, 0, 9, 0, 0, 8],
#     [0, 6, 0, 0, 0, 0, 0, 0, 0],
#     [1, 0, 0, 0, 0, 7, 0, 0, 0],
#     [0, 0, 9, 0, 0, 0, 2, 0, 0], 
#     [0, 0, 0, 5, 0, 0, 0, 0, 4],
#     [0, 0, 0, 0, 0, 0, 0, 2, 0],
#     [5, 0, 0, 6, 0, 0, 3, 4, 0],
#     [3, 4, 0, 2, 0, 0, 0, 0, 0],
# ]
# solve_sudoku(puzzle)
# print(puzzle)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


'''
# Automation for killer sudoku website works, however the rules of Killer Sudoku are
# not the same as normal Sudoku, thus the backtracking algorithm above does not work for
# this type of puzzle.
# To-Do: Create a working algorithm

# Killer Sudoku
driver.get('https://www.killersudoku.com/')

# press 'q' to run program
while True:
    if keyboard.is_pressed('q'):
        break

# get numbers already filled
filled = WebDriverWait(driver, timeout=10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'cell'))
)
filledNums = []
for num in filled:
    filledNums.append(int(num.get_attribute('value')))

# get all spots
cells = WebDriverWait(driver, timeout=10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'gridCell'))
)

# start filling the board up using the pre-filled numbers we found
i = 0
board = []
for cell in cells:
    # clickable attribute is '0' if filled and '1' if empty
    isEmpty = int(cell.get_attribute('clickable'))
    # Check if grid is empty, add a 0 if so, else add the next available filled number
    if isEmpty:
        board.append(0)
    else:
        board.append(filledNums[i])
        i += 1

# reshape the board into a regular 9x9 grid using numPy
board = np.reshape(board, (9, 9))
solve_sudoku(board)

# for every cell
for cell in cells:
    # skip elements already filled
    if cell.get_attribute('clickable') == '0': continue

    # get the coordinates of every cell, y is row and x is col
    r = int(cell.get_attribute('y'))
    c = int(cell.get_attribute('x'))
    
    cell.click()
    pyautogui.write(str(board[r][c]), _pause = False)

'''
# BigBangPlay Sudoku
driver.get('https://www.bigbangplay.com/en/games/sudoku/')

# press 'q' to run program
while True:
    if keyboard.is_pressed('q'):
        break

filledCells = WebDriverWait(driver, timeout=10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'frozen'))
)
filledNums = []
for num in filledCells:
    filledNums.append(int(num.get_attribute('value')))

# get all spots
toFill = WebDriverWait(driver, timeout=10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'toFill'))
        )

# start filling the board up using the pre-filled numbers we found
i = 0
board = [ 0 for _ in range(81)]
for filled in filledCells:
    # get index value of filled cell
    idx = filled.get_attribute('id')
    idx = idx[3:] # remove first 3 characters the 'val' and keep only the idx following it
    idx = int(idx) # convert to integer
    board[idx] = filledNums[i]
    i += 1

# reshape the board into a regular 9x9 grid using numPy
board = np.reshape(board, (9, 9))
solve_sudoku(board)

# for every cell
for cell in toFill:
    # get the coordinates of every cell, id gives us cell number in order from left to right
    idx = cell.get_attribute('id')
    idx = idx[3:]
    idx = int(idx) # convert to integer
    r, c = divmod(idx, 9) # convert flattened index to row, col index
    
    cell.click()
    pyautogui.write(str(board[r][c]), _pause = False)


# Elite Sudoku
driver.get('https://www.elitesudoku.com/')

# press 'q' to run program
while True:
    if keyboard.is_pressed('q'):
        break

# press start button
start_button = WebDriverWait(driver, timeout=10).until(
    EC.element_to_be_clickable((By.ID, 'start-game'))
)
start_button.click()

# read in all numbers from sudoku puzzle
cells = WebDriverWait(driver, timeout=10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'cell'))
)
numbers = []

for cell in cells:
    # if empty value add it as a 0 else convert the string into a number and add that value
    value = 0 if cell.get_attribute('value') == '' else int(cell.get_attribute('value'))
    numbers.append(value)

# reshape our list into a 9 x 9 array using numPy
numbers = np.reshape(numbers, (9, 9))

# numbers above are read in by blocks so the first 9 numbers are actually the first
# 9 numbers of block 1 and not of the entire row, transforming number to board
board = []
for r in range(3):
    for c in range(3):
        for n in range(3):
            board.extend(numbers[3 * r + n][3 * c : 3 * c + 3])
board = np.reshape(board, (9, 9))

# solve sudoku puzzle!
solve_sudoku(board)

# getting solution from solved board and organizing it by blocks
# essentially reversing the process above when we retrived the numbers
solution = []
for r in range(3):
    for c in range(3):
        for n in range(3):
            solution.extend(board[3 * r + n][3 * c : 3 * c + 3])

cur_idx = 0
# click on each cell
for cell in cells:
    cell.click()
    # enter in number
    pyautogui.write(str(solution[cur_idx]), _pause = False)
    cur_idx += 1
