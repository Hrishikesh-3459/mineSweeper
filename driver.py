# Code starts at line 110

from random import randint

ROW = 10 # Defining the number of rows for a beginner level
COL = 10 # Defining the number of columns for a beginner level
NO_OF_BOMBS = 10 # Defining the number of bombs for a beginner level
FULL_LINE = 190 # Constant for design purposes

grid = [['0'] * COL for j in range(ROW)] # Creating a grid 
board = [["."] * COL for j in range(ROW)] # Creating a board, that the user will see


# Function to generate bombs at random locations in the grid
def gen_bombs():
    ctr = 0
    while True:
        row = randint(0, ROW-1)
        col = randint(0, COL-1)
        if (grid[row][col] != '*'):
            grid[row][col] = '*' # '*' Indicates a bomb in the grid
            ctr += 1
        if(ctr == NO_OF_BOMBS):
            break
        



# Function to print the grid
def print_grid():
    POS_INDICATOR = 10
    for i in range(POS_INDICATOR):
        print("   |", i, end="")
    print("   |")
    k = 0
    for i in range(ROW):
        print(k, end="")
        for j in range(COL):
            print("  |  " + str(grid[i][j]), end="")
        print("  |")
        k += 1

# Function to print the board that is visible to the user
def print_board():
    BORDER = 64
    POS_INDICATOR = 10
    for i in range(FULL_LINE):
        print("-", end="")
    print()
    for i in range(BORDER):
        print("_", end="")
    print()
    k = 0
    for i in range(POS_INDICATOR):
        print("   |", i, end="")
    print("   |")
    for i in range(ROW):
        print(k, end="")
        for j in range(COL):
            print("  |  " + str(board[i][j]), end="")
        print("  |")
        k += 1
    for i in range(BORDER):
        print("_", end="")
    print()


# function to calculate the number of bombs in the vicinity of the given cell whose coordianates (row, col) are passed
def check_count(row, col): 
    count = 0
    r = -1 # Row constant, to iterate around a given cell 
    while(r < 2): 
        c = -1 # Column constant, to iterate around a given cell
        while(c < 2): 
            if (row + r not in range(0,ROW) or col + c not in range(0,COL)): # Skips over boundry cases
                pass
            elif (grid[row + r][col + c] == '*'): # counts the number if bombs around the given cell
                count += 1
            c += 1
        r += 1
    return (count) # The number of bombs are returned

# This function iterates over every cell in the 2D list 'grid' and calculates the number of bombs near it
def get_index():
    for i in range(ROW):
        for j in range(COL):
            if (grid[i][j] != '*'):
                grid[i][j] = str(check_count(i,j))

            
# Recursive function, to print the value at user's input
def open_grid(row, col):
    board[row][col] = grid[row][col]
    if(board[row][col] == '0'):
        r = -1
        while(r < 2):  
            c = -1
            while(c < 2):
                if (row + r not in range(0,ROW) or col + c not in range(0,COL)):
                    pass
                elif (board[row+r][col+c] == '.'):
                    if (grid[row + r][col + c] == '0'):
                        open_grid(row + r, col + c)
                    board[row+r][col+c] = grid[row+r][col+c]
                c += 1
            r += 1

    
# Calling the functions
gen_bombs()
get_index()
print_grid() # This is just for beta testing, so that we know where the bombs are
print_board()

while True:
    row = int(input("Enter the row coordinate: "))
    col = int(input("Enter the col coordinate: "))
    open_grid(row,col)
    print_board()

    if (grid[row][col] == '*'):
        print_grid() # Have to change is so as to print only the bombs
        print("Bomb Found")
        print("Game Over")
        break
