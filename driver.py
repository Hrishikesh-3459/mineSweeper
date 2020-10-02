

import random


ROW = {1: 10, 2: 17, 3: 17}  # Defining the number of rows for a beginner level
# Defining the number of columns for a beginner level
COL = {1: 10, 2: 17, 3: 31}
# Defining the number of bombs for a beginner level
NO_OF_BOMBS = {1: 10, 2: 40, 3: 99}
FULL_LINE = 200  # Constant for design purposes
BORDER = {1: 67, 2: 110, 3: 194}
while True:
    difficulty = int(
        input("Choose difficulty: \n1: Easy \n2: Medium \n3: Hard\nEnter Your Choice: "))
    if (difficulty in [1, 2, 3]):
        break
    else:
        print("Invalid choice")

grid = [['0'] * COL[difficulty]
        for j in range(ROW[difficulty])]  # Creating a grid
# Creating a board, that the user will see
board = [["."] * COL[difficulty] for j in range(ROW[difficulty])]


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        # The only way we can know for sure if the given cells are all mines, if the numeber of cells and the number of mines are equal
        if self.count == len(self.cells) and self.count != 0:
            return self.cells

        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        # The only way we can know for sure if there are no mines in the cells is, if the count is 0
        if self.count == 0:
            return self.cells

        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        # If we know that the given cell is in the set of cells, we remove it and reduce the count by 1
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        return

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        # If the cell is in the set of cells, we just remove it
        if cell in self.cells:
            self.cells.remove(cell)
        return


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """

        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """

        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # Marking the cell as one of the moves made in the game
        self.moves_made.add(cell)
        # print(f"moves made = {self.moves_made}")

        # Marking the cell as a safe cell, and updating any sentences that contain the cell
        self.mark_safe(cell)

        cells = set()

        row = cell[0]
        col = cell[1]

        # Finding neighbours
        for i in [row - 1, row, row + 1]:
            for j in [col - 1, col, col + 1]:
                if i < 0 or j < 0 or i >= self.height or j >= self.width:
                    continue
                if (i, j) == cell or (i, j) in self.safes:
                    continue
                cells.add((i, j))

        sentence_obj = Sentence(cells, count)
        self.knowledge.append(sentence_obj)

        tmp_knowledge = self.knowledge.copy()
        self.inference()

        # As long as new Sentences are added to the knowledge base, we must loop through them
        while self.knowledge != tmp_knowledge:
            tmp_knowledge = self.knowledge
            self.inference()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        # Since we have to make safe moves, we can only loop through the safe cells, are return the cells that are not a mine and not a move that has already been made
        for cell in self.safes:
            if cell not in self.moves_made and cell not in self.mines:
                return cell

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        available = set()

        # We loop through all the cells, and any cells that are not a mine, and not a move that has already been made, we add them to the avaiable cells
        for h in range(self.height):
            for w in range(self.width):

                cell = (h, w)
                if (cell not in self.moves_made) and (cell not in self.mines):
                    available.add(cell)

        if len(available) == 0:
            return None

        # Returning a random value from the available cells
        return random.choice(tuple(available))

    def inference(self):
        # Updating all the sentences for mines
        for i in self.mines:
            self.mark_mine(i)

        # Updating all the sentences for safe cells
        for i in self.safes:
            self.mark_safe(i)

        # Updating the known safes and known mines according to the login in the sentence class
        for s in self.knowledge:
            safe_cells = s.known_safes()
            mine_cells = s.known_mines()

            self.safes = self.safes.union(safe_cells)

            self.mines = self.mines.union(mine_cells)

        # While looping through the sets, if we find a set that is a subset of another set, we will subtract the sets and the count
        new_sentences = []
        for setA in self.knowledge:
            for setB in self.knowledge:

                if setB.cells.issubset(setA.cells) and setA != setB:
                    new_set = setA.cells - setB.cells
                    new_count = setA.count - setB.count
                    new_obj = Sentence(new_set, new_count)
                    new_sentences.append(new_obj)

        # Adding the new sentences to knowledge base
        for sentence in new_sentences:
            if sentence not in self.knowledge:
                self.knowledge.append(sentence)


# Function to generate bombs at random locations in the grid
def gen_bombs():
    ctr = 0
    while True:
        row = random.randint(0, ROW[difficulty]-1)
        col = random.randint(0, COL[difficulty]-1)
        if (grid[row][col] != '*'):
            grid[row][col] = '*'  # '*' Indicates a bomb in the grid
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
    print("Number of bombs = ", NO_OF_BOMBS[difficulty])
    print("Try to get around all the cells without activating a bomb")
    print("Good Luck!")


# Function to print the grid
def print_grid():
    POS_INDICATOR = ROW[difficulty]

    for i in range(FULL_LINE):
        print("-", end="")
    print()

    for i in range(BORDER[difficulty]):
        print("_", end="")
    print()
    space = "      "
    k = 0
    print(space, end="")
    for i in range(POS_INDICATOR):
        print('|' + str(i).center(5), end="")
    print("|")

    for i in range(ROW[difficulty]):
        if (i < 10):
            space = "  "
        else:
            space = " "
        print(k, space, end="")
        for j in range(COL[difficulty]):
            print("  |  " + str(grid[i][j]), end="")
        print("  |")
        k += 1

    for i in range(BORDER[difficulty]):
        print("_", end="")
    print()
    bom_count = 0
    for i in grid:
        for j in i:
            if (j == '*'):
                bom_count += 1
    print("Number of bombs = ", bom_count)


# This function is called when the used activates a bomb, all of the bombs are printed and the game is declared to be over
def show_bombs(grid, board):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
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
    print(space, end="")
    for i in range(POS_INDICATOR):
        print('|' + str(i).center(5), end="")
    print("|")

    for i in range(ROW[difficulty]):
        if (i < 10):
            space = "  "
        else:
            space = " "
        print(k, space, end="")
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
    r = -1  # Row constant, to iterate around a given cell
    while(r < 2):
        c = -1  # Column constant, to iterate around a given cell
        while(c < 2):
            # Skips over boundry cases
            if (row + r not in range(0, ROW[difficulty]) or col + c not in range(0, COL[difficulty])):
                pass
            # counts the number if bombs around the given cell
            elif (grid[row + r][col + c] == '*'):
                count += 1
            c += 1
        r += 1
    return (count)  # The number of bombs are returned


# This function iterates over every cell in the 2D list 'grid' and calculates the number of bombs near it
def get_index():
    for i in range(ROW[difficulty]):
        for j in range(COL[difficulty]):
            if (grid[i][j] != '*'):
                grid[i][j] = str(check_count(i, j))


# Recursive function, to print the value at user's input
def open_grid(row, col):
    board[row][col] = grid[row][col]
    cell = (row, col)
    if cell not in ai_obj.moves_made:
        ai_obj.add_knowledge(cell, check_count(cell[0], cell[1]))
    if(board[row][col] == '0'):
        r = -1
        while(r < 2):
            c = -1
            while(c < 2):
                if (row + r not in range(0, ROW[difficulty]) or col + c not in range(0, COL[difficulty])):
                    pass
                elif (board[row+r][col+c] == '.'):
                    if (grid[row + r][col + c] == '0'):
                        open_grid(row + r, col + c)
                        cell = (row + r, col + c)
                        if cell not in ai_obj.moves_made:
                            ai_obj.add_knowledge(
                                cell, check_count(row + r, col + c))
                    board[row+r][col+c] = grid[row+r][col+c]
                    cell = (row + r, col + c)
                    if cell not in ai_obj.moves_made:
                        ai_obj.add_knowledge(
                            cell, check_count(row + r, col + c))
                c += 1
            r += 1


# Calling the functions

gen_bombs()
get_index()
# print_grid()  # This is just for beta testing, so that we know where the bombs are
intro()
print_board()
ai_obj = MinesweeperAI(height=ROW[difficulty], width=COL[difficulty])


chances = 0

while True:
    chances += 1
    safe_move = ai_obj.make_safe_move()
    flag = False

    if safe_move != None:
        inp = input("Do you want AI to make safe move?(y/n): ")
        if inp == "y":
            flag = True
            print(f"AI making safe move at {safe_move}")
            row = safe_move[0]
            col = safe_move[1]
        else:
            row = int(input("Enter the row coordinate: "))
            col = int(input("Enter the col coordinate: "))
    else:
        inp = input("No safe moves available, make random move?(y/n): ")
        if inp == "y":
            flag = True
            random_move = ai_obj.make_random_move()
            print(f"AI making random move at {random_move}")
            row = random_move[0]
            col = random_move[1]
        else:
            row = int(input("Enter the row coordinate: "))
            col = int(input("Enter the col coordinate: "))

    if (board[row][col].isdigit()):  # checks if input already given
        print("Oops.. Looks like cell is already open. Enter new coordinates")
        continue

    # checks if input cell is a flag, and asks the used if they want to unflag it
    if (board[row][col] == "F"):
        uf = input("Do you want to unflag or open? (uf/o) ")
        if (uf == 'uf'):  # replaces the 'F' with a '.'
            board[row][col] = '.'
            print_board()
            continue

        elif (uf == 'o'):
            open_grid(row, col)  # opens the grid
            ai_obj.add_knowledge((row, col), check_count(row, col))
            if (end_game(row, col)):
                break
            print_board()
            continue

        else:
            chances -= 1  # kind of error handling, I admit it isn't done in a good way :|
            print("Invalid choice")
            continue
    if flag == False:
        f = input("Do you want to flag or open the cell? (f/o) ")
    else:
        f = "o"

    if (f == 'f'):
        board[row][col] = 'F'
    elif(f == 'o'):
        open_grid(row, col)
        ai_obj.add_knowledge((row, col), check_count(row, col))
    else:
        chances -= 1
        print("Invalid choice")
        continue

    if (end_game(row, col)):
        break
    print_board()
