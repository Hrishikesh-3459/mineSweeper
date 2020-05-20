
from random import randint

ROW = {1: 10, 2: 17, 3:17} # Defining the number of rows for a beginner level
COL = {1: 10, 2: 17, 3: 31} # Defining the number of columns for a beginner level
NO_OF_BOMBS = {1: 10, 2: 40, 3: 99} # Defining the number of bombs for a beginner level
FULL_LINE = 200 # Constant for design purposes
BORDER = {1: 67, 2: 110, 3: 194} 
while True:
    difficulty = int(input("Choose difficulty: \n1: Easy \n2: Medium \n3: Hard\nEnter Your Choice: "))
    if (difficulty in [1,2,3]):
        break
    else:
        print("Invalid choice")

grid = [['0'] * COL[difficulty] for j in range(ROW[difficulty])] # Creating a grid 
board = [["."] * COL[difficulty] for j in range(ROW[difficulty])] # Creating a board, that the user will see


# Function to generate bombs at random locations in the grid
def gen_bombs():
    ctr = 0
    while True:
        row = randint(0, ROW[difficulty]-1)
        col = randint(0, COL[difficulty]-1)
        if (grid[row][col] != '*'):
            grid[row][col] = '*' # '*' Indicates a bomb in the grid
            ctr += 1
        if(ctr == NO_OF_BOMBS[difficulty]):
            break

# Function to give the introduction message
def intro():
    st = "Welcome to Minesweeper game"
    ste = st.center(FULL_LINE, "-")
    print(ste)
    print("'.' indicate unexplored coordinates")
    print("'F' would appear over a cell if you decide to flag it")
    print("The game ends if you find a bomb")
    print("Number of bombs = ",NO_OF_BOMBS[difficulty])
    print("Try to get around all the cells without activating a bomb")
    print("Good Luck!")
    

# Function to print the grid
# def print_grid():
#     POS_INDICATOR = ROW[difficulty]

#     for i in range(FULL_LINE):
#         print("-", end="")
#     print()

#     for i in range(BORDER[difficulty]):
#         print("_", end="")
#     print()
#     space = "      "
#     k = 0
#     print(space, end = "")
#     for i in range(POS_INDICATOR):
#         print('|' + str(i).center(5), end="")
#     print("|")

#     for i in range(ROW[difficulty]):
#         if (i < 10):
#             space = "  "
#         else:
#             space = " "
#         print(k , space, end="")
#         for j in range(COL[difficulty]):
#             print("  |  " + str(grid[i][j]), end="")
#         print("  |")
#         k += 1

#     for i in range(BORDER[difficulty]):
#         print("_", end="")
#     print()
#     bom_count = 0
#     for i in grid:
#         for j in i:
#             if (j == '*'):
#                 bom_count += 1
#     print("Number of bombs = ",bom_count)
        

# This function is called when the used activates a bomb, all of the bombs are printed and the game is declared to be over
def show_bombs(grid, board):
    for i in range(len(grid)):
        for j in range(len(grid)):
            if (grid[i][j] == '*' and board[i][j] != 'F'):
                board[i][j] = '*'
    print_board()


# The game ends if the user selects a cell which is a bomb OR when all if the non bomb cells are open
def end_game(row, col):
    if (grid[row][col] == '*' and board[row][col] != 'F'):
        show_bombs(grid, board) 
        print("Bomb Found")
        print("Game Over")
        print("Chances: ", chances)
        return True

    count = 0
    for i in board:
        count += i.count('.') 
        count += i.count('F')
    print(count)
    if (count == NO_OF_BOMBS[difficulty]):
        print("You Won")
        print("Game Over")
        print("Chances: ", chances)
        return True

    



# Function to print the board that is visible to the user
def print_board():
    
    POS_INDICATOR = ROW[difficulty]
    if (difficulty == 3):
        POS_INDICATOR = 31

    for i in range(FULL_LINE):
        print("-", end="")
    print()

    for i in range(BORDER[difficulty]):
        print("_", end="")
    print()
    space = "      "
    k = 0
    print(space, end = "")
    for i in range(POS_INDICATOR):
        print('|' + str(i).center(5), end="")
    print("|")

    for i in range(ROW[difficulty]):
        if (i < 10):
            space = "  "
        else:
            space = " "
        print(k , space, end="")
        for j in range(COL[difficulty]):
            print("  |  " + str(board[i][j]), end="")
        print("  |")
        k += 1

    for i in range(BORDER[difficulty]):
        print("_", end="")
    print()





# function to calculate the number of bombs in the vicinity of the given cell whose coordianates (row, col) are passed
def check_count(row, col): 
    count = 0
    r = -1 # Row constant, to iterate around a given cell 
    while(r < 2): 
        c = -1 # Column constant, to iterate around a given cell
        while(c < 2): 
            if (row + r not in range(0,ROW[difficulty]) or col + c not in range(0,COL[difficulty])): # Skips over boundry cases
                pass
            elif (grid[row + r][col + c] == '*'): # counts the number if bombs around the given cell
                count += 1
            c += 1
        r += 1
    return (count) # The number of bombs are returned



# This function iterates over every cell in the 2D list 'grid' and calculates the number of bombs near it
def get_index():
    for i in range(ROW[difficulty]):
        for j in range(COL[difficulty]):
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
                if (row + r not in range(0,ROW[difficulty]) or col + c not in range(0,COL[difficulty])):
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
# print_grid() # This is just for beta testing, so that we know where the bombs are
intro()
print_board()


chances = 0

while True:
    chances += 1
    row = int(input("Enter the row coordinate: "))
    col = int(input("Enter the col coordinate: "))
    
    if (board[row][col].isdigit()): # checks if input already given
        print("Oops.. Looks like cell is already open. Enter new coordinates")
        continue
    
    if (board[row][col] == "F"): # checks if input cell is a flag, and asks the used if they want to unflag it
        uf = input("Do you want to unflag or open? (uf/o) ")
        if (uf == 'uf'): # replaces the 'F' with a '.'
            board[row][col] = '.'
            print_board()
            continue

        elif (uf == 'o'):
            open_grid(row,col) # opens the grid
            if (end_game(row,col)):
                break
            print_board()
            continue
        
        else:
            chances -= 1 # kind of error handling, I admit it isn't done in a good way :|
            print("Invalid choice")
            continue

    
    f = input("Do you want to flag or open the cell? (f/o) ")
    
    if (f == 'f'):
        board[row][col] = 'F'
    elif(f == 'o'):
        open_grid(row,col)
    else:
        chances -= 1
        print("Invalid choice")
        continue

    if (end_game(row,col)):
        break
    print_board()
