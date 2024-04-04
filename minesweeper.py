import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

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
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


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
            # Step 1: Mark the cell as moved
            self.moves_made.add(cell)

            # Step 2: Mark the cell as safe
            self.mark_safe(cell)

            # Step 3: Add new knowledge to the AI
            i, j = cell
            new_knowledge = []
            neighbors = set()
            # Iterate over neighboring cells
            for x in range(max(0, i - 1), min(self.height, i + 2)):
                for y in range(max(0, j - 1), min(self.width, j + 2)):
                    # Add to the cell collection if the cell is not yet explored
                    # and is not the mine already known
                    # If we know that it is safe we ignore it
                    if (x,y) in self.safes:
                        continue

                    # If we know that it is a mine we ignore it
                    # When excluding a known mine cell, decrease the count by 1
                    if (x,y) in self.mines:
                        count -= 1
                        continue
                    # If it not the same cell we add it
                    if (x, y) != cell:
                        neighbors.add((x, y))


            # Add new sentence to the knowledge base if neighbors are valid and their count is not 0
            if neighbors and count > 0:
                self.knowledge.append(Sentence(neighbors, count))
            
            # We have created new knowledge that we will have to go through and analyze
            knowledge_added = True
            safes = set()
            mines = set()

            # Step 4: Mark additional cells
            while knowledge_added:
                knowledge_added = False


                # Gather the known safes and mines from all the sentences in our KB
                for sentence in self.knowledge:
                    safes = safes.union(sentence.known_safes())
                    mines = mines.union(sentence.known_mines())

                # Mark all the safes including the new ones as safe:
                if safes:
                    knowledge_changed = True
                    for safe in safes:
                        self.mark_safe(safe)
                # Same proceedure but with mines
                if mines:
                    knowledge_changed = True
                    for mine in mines:
                        self.mark_mine(mine)
                
                # Remove any empty sentences from knowledge base:
                empty = Sentence(set(), 0)
                self.knowledge[:] = [x for x in self.knowledge if x != empty]

                # Step 5: Infer new knowledge
                # We go through all diferent sentences present on the knowledge base 
                for sentence1 in self.knowledge:
                    for sentence2 in self.knowledge:
                        if sentence1 == sentence2:
                            continue
                        # We check if the sentence 1 is a subset of the sentence 2
                        if sentence1.cells.issubset(sentence2.cells):
                            # If it is we apply the formula set2 - set1 = count2 - count1
                            new_sentence_cells = sentence2.cells - sentence1.cells
                            new_sentence_count = sentence2.count - sentence1.count
                            # Now we create the new infered sentence
                            new_sentence = Sentence(new_sentence_cells, new_sentence_count)
                            # We check if our new inference is not in the knowledge base
                            if new_sentence not in self.knowledge:
                                # If it is not we add it
                                self.knowledge.append(new_sentence)
                                # As new knowledge was added we will need to analyze it again
                                knowledge_added = True


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # We select all the safe moves that were not yet performed
        safe_moves_availables = self.safes - self.moves_made
        if safe_moves_availables:
            return random.choice(list(safe_moves_availables))
        # Otherwise no guaranteed safe moves can be made
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        for i in range(self.height):
            for j in range(self.width):
                cell = (i,j)
                if cell not in self.moves_made and cell not in self.mines:
                    return cell
        return None
