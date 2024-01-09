import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=15, width=15, mines=40):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


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
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        if cell in self.cells:
            self.count -= 1
        self.cells.discard(cell)
        

    def mark_safe(self, cell):
        self.cells.discard(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=15, width=15):

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
        #Add to moves made
        self.moves_made.add(cell)

        #Add to safe cells
        self.safes.add(cell)

        #Create set of surrounding cells, within bounds of game
        surroundingCells = set()
        for i in range(cell[0]-1, cell[0]+2):
            for j in range(cell[1]-1, cell[1]+2):
                if i >= 0 and i < self.width and j >=0 and j < self.height:
                    surroundingCells.add((i, j))

        #Remove current cell, and cells marked as safe or mine. Remove 1 from count for every mine found
        newCount = count

        surroundingCells.remove(cell)
        for safeCell in self.safes:
            surroundingCells.discard(safeCell)
        for mineCell in self.mines:
            if mineCell in surroundingCells:
                surroundingCells.remove(mineCell)
                newCount -= 1

        #Create and add sentence with surrounding cell knowledge
        newSentence = Sentence(surroundingCells, newCount)
        self.knowledge.append(newSentence)

        #Update knowledge base with new inferences
        while True:
            changeCounter = 0

            #Create mine and safe sets
            inferMines = set()
            inferSafes = set()

            #Check if sentences can determine safe or mine cells, and add to sets
            for checkSentence in self.knowledge:
                if len(checkSentence.cells) > 0:

                    if len(checkSentence.cells) == int(checkSentence.count):
                        for cell in checkSentence.cells:
                            inferMines.add(cell)

                    if int(checkSentence.count) == 0:
                        for cell in checkSentence.cells:
                            inferSafes.add(cell)

            #Update knowledge base with inferred sets
            for cell in inferMines:
                self.mark_mine(cell)
                changeCounter += 1

            for cell in inferSafes:
                self.mark_safe(cell)
                changeCounter += 1

            #Delete empty sentences from knowledge base
            for checkSentence in self.knowledge:
                if len(checkSentence.cells) == 0:
                    self.knowledge.remove(checkSentence)

            #Check each sentence for subsets. Add new sentence based on subsets      
            inferNewSentences = []      
            for checkSentenceA in self.knowledge:                  
                    for checkSentenceB in self.knowledge:

                        if checkSentenceA != checkSentenceB and checkSentenceB.cells.issubset(checkSentenceA.cells):
                            subtractedSentence = Sentence(checkSentenceA.cells.difference(checkSentenceB.cells),
                                                        checkSentenceA.count - checkSentenceB.count)

                            if subtractedSentence not in self.knowledge:
                                inferNewSentences.append(subtractedSentence)

            #Update knowledge with new sentences    
            for item in inferNewSentences:
                self.knowledge.append(item)
                changeCounter += 1

            #Break if no changes were made
            if changeCounter == 0:
                break


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        #Create set of safe moves that have not been made
        moveSet = set()
        for move in self.safes:
            if move not in self.moves_made:
                moveSet.add(move)

        #Return random choice from set
        if len(moveSet) == 0:
            return None
        else:
            randChoice = random.choice(list(moveSet))
            return randChoice
        


        

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        #Create set of all moves not in self.mines or self.moves_made
        moveSet = set()
        for i in range(0, self.width):
            for j in range(0, self.height):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    moveSet.add((i, j))

        #Return random choice from set
        if len(moveSet) == 0:
            return None
        else:
            return random.choice(list(moveSet))