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
        new_knowledge = []
        neighbors = set()
        i, j = cell
        
        # Iterate over neighboring cells
        # We search in each row and column but taking into account the limits. -> Remember superior limit not included
        for x in range(max(0, i - 1), min(self.height, i + 2)):
            for y in range(max(0, j - 1), min(self.width, j + 2)):
                neighbor = (x, y)
                # Skip if the neighbor is the cell itself or already moved
                if neighbor != cell and neighbor not in self.moves_made:
                    neighbors.add(neighbor)

        # Add new sentence to the knowledge base if neighbors are valid and their count is not 0
        if neighbors and count > 0:
            # Filter out any cells that are known to be mines or safes
            new_sentence_cells = {n for n in neighbors if n not in self.mines and n not in self.safes}
            self.knowledge.append(Sentence(neighbors, count))

        # Step 4: Mark additional cells
        for sentence in self.knowledge:
            known_mines = sentence.known_mines()
            known_safes = sentence.known_safes()
            # (Here we use the |= operator that is used to perform an union of sets. 
            # It adds all elements of the right-hand side set to the left-hand side set, 
            # but without duplicating elements.)
            if known_mines:
                self.mines |= known_mines
            if known_safes:
                self.safes |= known_safes

        # Step 5: Infer new knowledge
        new_knowledge = []
        for sentence in self.knowledge:
            if not sentence.cells:
                continue
            # If our sentence count is 0 it means that all the cells in that sentence are safe
            # So we mark them as safe
            if sentence.count == 0:
                for safe_cell in sentence.cells.copy():
                    self.mark_safe(safe_cell)
            # If not but the amount of cells is equal to the count then we know that all of them are mines
            # So we mark them as mine
            elif len(sentence.cells) == sentence.count:
                for mine_cell in sentence.cells.copy():
                    self.mark_mine(mine_cell)
            # If neither inference can be made we store the sentence as it is
            else:
                new_knowledge.append(sentence)
        # We replace the agent knowledge with this new knowledge
        self.knowledge = new_knowledge
        # With this new knowledge we can make inferences of their subsets.
        self.infer_from_sentences()

        # Now we can infer additional safe cells and mines
        for sentence in self.knowledge:
            # Check if the count is 0 and the sentence has cells
            if sentence.count == 0 and sentence.cells:
                for cell in sentence.cells.copy():
                    # Check if the cell is not already marked as safe
                    if cell not in self.safes:
                        self.mark_safe(cell)
            # Check if the count is equal to the number of cells in the sentence
            elif len(sentence.cells) == sentence.count and sentence.cells:
                for cell in sentence.cells.copy():
                    # Check if the cell is not already marked as a mine
                    if cell not in self.mines:
                        self.mark_mine(cell)

        # Step 6: Combine multiple sentences to draw conclusions
        self.combine_sentences()

    def infer_from_sentences(self):
        # We go through all diferent sentences present on the knowledge base recursively 
        new_sentences_added = 0
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
                        new_sentences_added += 1
        # We recursively call the function again if we added a new sentence
        if new_sentences_added > 0:
            self.infer_from_sentences()

    def combine_sentences(self):
        """
        Combines multiple sentences to draw conclusions.

        This function iterates over all pairs of distinct sentences
        in the knowledge base and checks if one sentence is a subset
        of another. If such a subset relationship is found, it creates
        a new sentence representing the difference between the two sets,
        and adds it to the knowledge base if it is not already present.

        This process continues recursively until no new sentences
        can be inferred.
        """
        # Flag to indicate if any new sentences were added
        combined = True
        
        # Iterate until no new sentences are added
        while combined:
            combined = False
            
            # Iterate over each pair of sentences in the knowledge base
            for i, sentence1 in enumerate(self.knowledge):
                for j, sentence2 in enumerate(self.knowledge):
                    # Skip if the same sentence or if one is subset of the other
                    if i == j or sentence1.cells.issubset(sentence2.cells):
                        continue

                    # Check if sentence2 is a subset of sentence1
                    if sentence2.cells.issubset(sentence1.cells):
                        # Infer new sentence representing the difference
                        new_sentence_cells = sentence1.cells - sentence2.cells
                        new_sentence_count = sentence1.count - sentence2.count
                        new_sentence = Sentence(new_sentence_cells, new_sentence_count)

                        # Check if the new sentence is not already in knowledge base
                        if new_sentence not in self.knowledge:
                            # Add new sentence and set combined to True
                            self.knowledge.append(new_sentence)
                            combined = True

                            # Break the inner loop as a new sentence is added
                            break

                # Break the outer loop if a new sentence is added
                if combined:
                    break

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Check if there are any safe moves available
        if not self.safes:
            return None
        
        # Iterate through the set of safe cells and return the first one that has not been chosen
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        
        # If all safe cells have been chosen, return None
        return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Create a list to store possible moves
        possible_moves = []

        # Iterate through all cells on the board
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                # Check if the cell is not already chosen and not a mine
                if cell not in self.moves_made and cell not in self.mines:
                    # Add the cell to the list of possible moves
                    possible_moves.append(cell)

        # Check if there are any possible moves available
        if possible_moves:
            # Choose a random move from the list of possible moves
            return random.choice(possible_moves)
        else:
            # If no possible moves are available, return None
            return None

