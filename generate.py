import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
        constraints; in this case, the length of the word.)
        """
        for variable in self.crossword.variables:
            # Get the length of the variable
            length = variable.length
            # Get the domain of the variable
            domain = self.domains[variable]
            # Create a new domain containing only words of the same length
            new_domain = set()
            for word in domain:
                if len(word) == length:
                    new_domain.add(word)
            # Update the domain of the variable
            self.domains[variable] = new_domain


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        # We check if there is overlaping between the variables(Words)
        overlap = self.crossword.overlaps[x, y]
        if overlap is not None:
            # If there is any overlap we want the position of it
            i, j = overlap
            new_domain_x = set()
            # We check the domain of X (Possible values of X)
            for value_x in self.domains[x]:
                # We want the possible values of X and the possible values of Y
                # that have the same letter in the position of overlap i,j 
                if any(value_y[i] == value_x[j] for value_y in self.domains[y]):
                    # We store them in a new domain
                    new_domain_x.add(value_x)
                else:
                    revised = True
            if revised:
                # If there was any change we update the domain of X
                self.domains[x] = new_domain_x
        return revised


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            # If arcs is empy we create the queu using all the pairs of word, neighbor word
            arcs = [(x, y) for x in self.crossword.variables for y in self.crossword.neighbors(x)]
        # We process untill the queu is empty
        while arcs:
            # remove one pair
            x, y = arcs.pop(0)
            # We check that pair using the previous function
            if self.revise(x, y):
                # If the domain is 0 it means that there is no solution
                if len(self.domains[x]) == 0:
                    return False
                # For each new addition to the domain we should add it to the queu
                for z in self.crossword.neighbors(x):
                    if z != y:
                        arcs.append((z, x))
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # We take each variable of the crossword
        for variable in self.crossword.variables:
            # We check if that variable is present in the dictionary
            # this means that it has some value assigned
            if variable not in assignment:
                return False
        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Verify that all the words are different
        # We create a set of values(unique values) because each variable can have only a word and each one 
        # must be different between them
        # So if the lenght is different it means that we have repeated words (which is incorrect)
        if len(set(assignment.values())) != len(assignment):
            return False

        # Verifying that each word is the correct length
        # .items returns ---> [('Variable1', 'WORD1'), ('Variable2', 'WORD2'), ('Variable3', 'WORD3')]
        for variable, word in assignment.items():
            # if the lenghts are different then the word does not fit correctly
            # therefore is incorrect
            if len(word) != variable.length:
                return False

        # Conflicts between neighbors
        for variable, word in assignment.items():
            # We get the neighbors of the varible
            for neighbor in self.crossword.neighbors(variable):
                # We check that the neighbor has words assigned
                if neighbor in assignment:
                    # We take the overlaps coordinates X,Y
                    i, j = self.crossword.overlaps[variable, neighbor]
                    # If the two words have different letters where its suppossed to be a similar one
                    # then we have a conflict, we have chosen the incorrect words
                    if word[i] != assignment[neighbor][j]:
                        return False

        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Function to count the amount of values eliminated 
        def count_eliminated_values(value):
            count = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment and value in self.domains[neighbor]:
                    count += 1
            return count

        # Ordenar los valores del dominio de la variable según el número de valores eliminados para los vecinos no asignados
        return sorted(self.domains[var], key=count_eliminated_values)


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # We gather all the variables not yet assigned
        unassigned_variables = [var for var in self.crossword.variables if var not in assignment]
        
        # We order them by the number of values left in their domains
        unassigned_variables.sort(key=lambda var: len(self.domains[var]))
        
        # We obtain the amount of values that the variable with the least amount of values left in its domain has
        min_remaining_values = len(self.domains[unassigned_variables[0]])
        
        # We search for other variables with the same minimum number of values left
        min_remaining_variables = [var for var in unassigned_variables if len(self.domains[var]) == min_remaining_values]
        
        # If there is a tie, we choose the one with the largest degree(most amount of neighbors)
        if len(min_remaining_variables) > 1:
            max_degree_variable = max(min_remaining_variables, key=lambda var: len(self.crossword.neighbors(var)))
            return max_degree_variable
        
        # if there is no tie we return the variable with the least amount of values under its domain
        return min_remaining_variables[0]


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # If the assignment is complete, return it
        if self.assignment_complete(assignment):
            return assignment
        
        # Select an unassigned variable
        var = self.select_unassigned_variable(assignment)
        
        # Iterate over the values in the domain of the selected variable
        for value in self.order_domain_values(var, assignment):
            # Assign the value to the variable
            assignment[var] = value
            
            # Check if the assignment is consistent
            if self.consistent(assignment):
                # Make a recursive call with the new assignment
                result = self.backtrack(assignment)
                
                # If a solution is found, return it
                if result is not None:
                    return result
            
            # If the assignment is not consistent, undo it
            assignment.pop(var)
        
        # If no solution is found, return None
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
