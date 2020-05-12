from random import randint

B_ROW = 10 # Defining the number of rows for a beginner level
B_COL = 10 # Defining the number of columns for a beginner level
B_NO_OF_BOMBS_BOMBS = 10 # Defining the number of bombs for a beginner level

grid = [[0] * B_COL for j in range(B_ROW)] # Creating a grid 


# Function to generate bombs at random locations in the grid
def gen_bombs():
    for i in range(B_NO_OF_BOMBS_BOMBS+1):
        location = {}
        location['row'] = randint(0, B_ROW-1)
        location['column'] = randint(0, B_COL-1)
        grid[location['row']][location['column']] = '*' # '*' Indicates a bomb in the grid


# Function to print the grid
def print_grid():
    POS_INDICATOR = 10
    for i in range(POS_INDICATOR):
        print("   |", i, end="")
    print("   |")
    k = 0
    for i in range(B_ROW):
        print(k, end="")
        for j in range(B_COL):
            print("  |  " + str(grid[i][j]), end="")
        print("  |")
        k += 1


# function to calculate the number of bombs in the vicinity of the given cell whose coordianates (row, col) are passed
def check_count(row, col):
    # Haven't yet figured out the logic for corner cases, it's a work in progress :)
    if (row == 0 or row == 9 or col == 0 or col == 9):
        return '#' 
    count = 0
    k = -1
    for i in range(3): # Used 3 to iterate over the cells above and below the current cell
        r = -1
        for j in range(3): # Used 3 to iterate over the cells on the left and right of the current cell
            if (grid[row + k][col + r] == '*'):
                count += 1
            r += 1
        k += 1
    return (count) # The number of bombs are returned

# This function iterates over every cell in the 2D list 'grid' and calculates the number of bombs near it
def get_index():
    for i in range(B_ROW):
        for j in range(B_COL):
            if (grid[i][j] == '*'):
                continue
            grid[i][j] = check_count(i,j)




# Calling the functions
gen_bombs()
get_index()
print_grid()
