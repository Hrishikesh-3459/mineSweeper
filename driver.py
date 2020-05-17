
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

def intro():
    st = "Welcome to Minesweeper game"
    ste = st.center(FULL_LINE, "-")
    print(ste)
    print("'.' indicate unexplored coordinates")
    print("'F' would appear over a cell if you decide to flag it")
    print("The game ends if you find a bomb")
    print("Try to get around all the cells without activating a bomb")
    print("Good Luck!")
    

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
        

# This function is called when the used activates a bomb, all of the bombs are printed and the game is declared to be over
def show_bombs(grid, board):
    for i in range(len(grid)):
        for j in range(len(grid)):
            if (grid[i][j] == '*' and board[i][j] != 'F'):
                board[i][j] = '*'
    print_board()


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
intro()
print_board()


chances = 0

while True:
    chances += 1
    f = input("Do you want to flag? (y/n) ")
    row = int(input("Enter the row coordinate: "))
    col = int(input("Enter the col coordinate: "))
    if (f == 'y'):
        board[row][col] = 'F'
    else:
        open_grid(row,col)
        if (grid[row][col] == '*'):
            show_bombs(grid, board) # Have to change is so as to print only the bombs
            print("Bomb Found")
            print("Game Over")
            print("Chances: ", chances)
            break
    print_board()

    
