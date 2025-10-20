import sys

from crossword import *
from crossword import Variable
from crossword import Crossword


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
        #assignment = {"Variable1" : "Word", "Variable2" : "Word2", ...}
        #Variable = (i, j, direction, length)
        #Ensuring node consistency is achieved when for every variable, each value in its domain is consistent with the variables unary constraints.
        #This means making sure that every value in a variable domain has the same number of letters as the variable length.
        #self.domains = {var: self.crossword.words.copy() for var in self.crossword.variables}
        #self.domains = {var(0,0,ACROSS,3): {"CAT", "DOG", "MOUSE"}, var(1,0,DOWN,4): {"FISH", "BIRD"}}
        
        for var in self.domains:
            to_remove = set()
            for word in self.domains[var]:
                if len(word) != var.length:
                    to_remove.add(word)
            self.domains[var] -= to_remove

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        #Start by assuming no revision has been made
        revision = False
        overlap = self.crossword.overlaps[x, y]
        if overlap is None:
            return revision
        elif overlap is not None:
            intersect_index_x, intersect_index_y = overlap
            to_remove = set()
            for word_x in self.domains[x]:
                found = False
                for word_y in self.domains[y]:
                    if word_x[intersect_index_x] == word_y[intersect_index_y]:
                        found = True
                        break
                if not found:
                    to_remove.add(word_x)
                    revision = True
            self.domains[x] -= to_remove
            return revision


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is  None:
            arcs = []
            for x in self.crossword.variables:
                for y in self.crossword.neighbors(x):
                    arcs.append((x, y))
            while arcs:
                (x,y) = arcs.pop(0)
                if self.revise(x,y):
                    if len(self.domains[x]) == 0:
                        return False
                    for z in self.crossword.neighbors(x):
                        if z != y:
                            arcs.append((z, x))
            return True
        else:
            while arcs:
                (x,y) = arcs.pop(0)
                if self.revise(x,y):
                    if len(self.domains[x]) == 0:
                        return False
                    for z in self.crossword.neighbors(x):
                        if z != y:
                            arcs.append((z, x))
            return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        #assigment its a dictionary mapping variables to words
        #Example: assigmnt = {"Variable1" : "Word", "Variable2" : "Word2", ...}
        
        for var in self.crossword.variables:
            if var not in assignment:
                return False
        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        #Assigment is a dictionary mapping variables to words
        #Example: assigmnt = {"Variable1" : "Word", "Variable2:" : "Word2", ...}
        #The assigments is consistent if all values are different, correct length and there are no conflicts between neighboring variables.
        
        #if len word of value in var 1 inside dic assigment is not equal to length of var1 return false
        #Var1 is a object of class variable with attributes i,j,direction,length
        for var1 in assignment:
            if len(assignment[var1]) != var1.length:
                return False
            
        for var1 in assignment:
            for var2 in assignment:
                if var1 != var2:
                    if assignment[var1] == assignment[var2]:
                        return False
                        
                    #Check overlaps
                    overlap = self.crossword.overlaps[var1, var2]
                    if overlap is not None:
                        index1, index2 = overlap
                        if assignment[var1][index1] != assignment[var2][index2]:
                            return False
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        value_counts = {}
        for value in self.domains[var]:
            count = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment:
                    overlap = self.crossword.overlaps[var, neighbor]
                    if overlap is not None:
                        index_var, index_neighbor = overlap
                        for neighbor_value in self.domains[neighbor]:
                            if value[index_var] != neighbor_value[index_neighbor]:
                                count += 1
            value_counts[value] = count
        return sorted(self.domains[var], key=lambda val: value_counts[val])
                

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_vars = [var for var in self.crossword.variables if var not in assignment]
        #Minimum Remaining values (MRV)
        mrv = min(unassigned_vars, key = lambda var: len(self.domains[var]))
        #Check for ties
        tied_vars = [var for var in unassigned_vars if len(self.domains[var]) == len(self.domains[mrv])]
        if len(tied_vars) == 1:
            return mrv
        else:
            #Heuristic: Degree
            return max(tied_vars, key = lambda var: len(self.crossword.neighbors(var)))
        

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            del assignment[var]
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
