# The Encoding class is used to solve the model
from lib204 import Encoding

# Var is an object used to store boolean conditions
from nnf import Var

# The iff method is used to determine the middle square's state
from nnf.operators import iff

class MinesweeperState:

    # The minesweeper state
    state = []

    # The expected result of this state (only used with pre-defined states)
    expected = None

    # This state's number for pre-defined states, or "new" for a user defined state
    state_num = ""

    '''
    Boolean condition guide:

    Each of the following lists will contain the boolean values for a specified
    condition for each square on the 5x5 board. Each square will be given a True
    or False value for each of these five conditions

    -x is a revealed spot where the number of adjacent mines is equal to the number
    of adjacent squares that we know are mines (x is 'satisfied'. This means that
    all of the adjacent unknown squares are safe)
        -This condition is used to check if the middle square is safe. We can only be
        sure of the safety of the middle square if there is at least one adjacent x
    -y is a revealed spot where the number of adjacent mines is equal to the number
    of adjacent known mines and the number of adjacent unrevealed squares (this
    means that every unknown square around a y square is a mine)
        -This condition is used to check if the middle square is a mine. We can only
        be sure the middle square is a mine if there is at least one adjacent y
    -m (mine) is a square that has not been revealed and we know it has a mine (a
    flag in a real game of minesweeper)
    -s (safe) is a square that has not been revealed and we know it does not have a
    mine (a square that you would click to reveal in a real game of minesweeper)
    -u (unknown) is a square that has not been revealed and we don't know if it is a
    mine or a safe spot

    Notes:
    -If a square is revealed, it can have 3 possible states:
        1. True x condition and False for every other condition
        2. True y condition and False for every other condition
        3. False for all conditions (the square is revealed but we aren't sure where
        all the adjacent mines are, i.e not an x or a y. For example, a square with
        2 adjacent mines but we only know where one of them is)

        Important: It is not possible in our case to have a True x condition and a
        True y condition. This would occur if a square is a satisfied x with no
        adjacent unknown squares; but this won't happen because the middle square is
        unknown and we only find x and y conditions for the inner ring of 8 squares

    -If a square is not revealed, it has to be one of the three revealed conditions:
        1. If we know the square is a mine, m is True and all other conditions are False
        2. If we know the square is safe, s is True and all other conditions are False
        3. If we don't know if the square is a mine or safe, u is True and all other
        conditions are False
    '''

    # The x boolean condition for each square
    x = [[],  # row 1
        [],  # row 2
        [],  # row 3
        [],  # row 4
        []]  # row 5

    # The y boolean condition for each square
    y = [[],  # row 1
        [],  # row 2
        [],  # row 3
        [],  # row 4
        []]  # row 5

    # The m boolean condition for each square
    m = [[],  # row 1
        [],  # row 2
        [],  # row 3
        [],  # row 4
        []]  # row 5

    # The u boolean condition for each square
    u = [[],  # row 1
        [],  # row 2
        [],  # row 3
        [],  # row 4
        []]  # row 5

    # The s boolean condition for each square
    s = [[],  # row 1
        [],  # row 2
        [],  # row 3
        [],  # row 4
        []]  # row 5

    # Encoding initialization
    E = Encoding()

    def __init__(self, new_state, num="new"):
        self.state = new_state[:]
        self.state_num = num
    

    def set_square(self, new_value, i, j):
        self.state[i][j] = new_value
    

    def set_row(self, new_row, i):
        self.state[i] = new_row[:]


    def test_state(self):
        """
        Tests this minesweeper states and prints:
            -A visual representation of the state
            -The state's satisfiability
            -The expected result of the state (for predefined states)
            -The result calculated by the encoding
            -A prompt to print all of the state variables
        """

        self.__create_encoding()  # Adds the constraints and state variables
        solution = self.E.solve()  # Solves the encoding
        
        self.print_state()

        # Prints if the encoding is satisfiable, the expected result and model result
        print("SATISFIABLE: " + str(self.E.is_satisfiable()) + "\n")
        if self.expected:
            print("Expected result:", self.expected)
        print("Model result: %s\n" % self.get_solution(solution))

        while True:
            print_solution = input("Would you like to see the full solution states (y/n)? ")
            try:
                print_solution.strip().lower()
                if print_solution == 'y':
                    # Prints the solution
                    # The format of this is the boolean values of u, m, x and y for
                    # each square as well as the s condition value for the middle square
                    print("\nSOLUTION:")
                    middle_squares = [1, 2, 3]
                    for i in middle_squares:
                        for j in middle_squares:
                            num = str(i) + str(j)
                            keyu = "u" + num
                            keym = "m" + num
                            keyx = "x" + num
                            keyy = "y" + num
                            print(keyu, solution[keyu])
                            print(keym, solution[keym])
                            print(keyx, solution[keyx])
                            print(keyy, solution[keyy])
                            if i == 2 and j == 2:
                                print("s22", solution["s22"])
                            print()
                    break
                elif print_solution == 'n':
                    break
                else:
                    print("Invalid input\n")
            except:
                print("Invalid input\n")
    

    def __create_encoding(self):
        """
        Calls all the functions in the correct order

        @param grid: 5x5 2-dimensional list minesweeper grid
        @type grid: list of 5 lists of 5 var objects
        """
        self.__set_initial_state()
        self.__set_truth_encodings()
    

    def __set_initial_state(self):
        """
        Sets the initial state of this minesweeper grid
        """
        grid_range = range(5)  # A range variable used to iterate through the grid

        # Instantiates Var objects for u, m and s cases for the 5x5 grid
        for i in grid_range:
            for j in grid_range:
                # These create objects for each condition and state in the form
                # mij, uij and sij. For example, m12 would be the condition that
                # the square at coordinates (1, 2) is a bomb (coordinates start
                # at (0, 0))
                self.m[i].append(Var('m' + str(i) + str(j)))
                self.u[i].append(Var('u' + str(i) + str(j)))
                self.s[i].append(Var('s' + str(i) + str(j)))

                # Each square's state is checked and constraints are added
                # The if conditional is used to ignore the center square since
                # we don't need constraints for it
                if not (i == 2 and j == 2):
                    state = self.state[i][j]
                    # Raises an exception if a square has an illegal value
                    if not (-2 <= state <= 8):
                        raise Exception('error: each square of the grid must have a'
                                        ' value between -2 and 8 inclusive. Square '
                                        '[%d][%d] has a value of %d' % (i, j, state))

                    if state == -2:  # mine
                        self.E.add_constraint(self.m[i][j])
                    else:
                        self.E.add_constraint(~self.m[i][j])

                    if state == -1:  # unknown
                        self.E.add_constraint(self.u[i][j])
                    else:
                        self.E.add_constraint(~self.u[i][j])

                    if state > -1:  # revealed square
                        self.E.add_constraint(self.s[i][j])
                    else:
                        self.E.add_constraint(~self.s[i][j])

        # Initializing x and y cases
        for i in grid_range:
            for j in grid_range:
                # We are only initializing the x and y truth values for the inner
                # 9 squares
                # The outer ring of squares can sometimes be determined for x and
                # y values, but that is beyond our scope
                if 0 < i < 4 and 0 < j < 4:
                    self.__set_x_truth(i, j)
                    self.__set_y_truth(i, j)
                else:
                    self.x[i].append(Var("x" + str(i) + str(j)))
                    self.y[i].append(Var("y" + str(i) + str(j)))


    def __set_x_truth(self, i, j):
        """
        Sets the x truth values a given square in a grid

        @param grid_setup: 5x5 2-dimensional list of a grid state
        @type grid_setup: list of 5 lists of 5 Var objects
        @param i: row number of the square
        @type i: integer (1 <= i <= 3)
        @param j: column number of the square
        @type j: integer (1 <= j <= 3)
        """

        # This constant list is used to quickly get the coordinates of adjacent squares
        coordinates = [[i - 1, j - 1], [i - 1, j], [i - 1, j + 1],
                       [  i  , j - 1],             [  i  , j + 1],
                       [i + 1, j - 1], [i + 1, j], [i + 1, j + 1]]
        counter = 0  # Used for counting the number of adjacent mines

        for n in range(len(coordinates)):
            adjacent_row = coordinates[n][0]
            adjacent_col = coordinates[n][1]
            # The following conditional checks if the nth adjacent square is a mine
            if self.state[adjacent_row][adjacent_col] == -2:
                counter += 1

        # Instantiates a Var object for the x condition at the given coordinate and
        # sets a constraint for it
        self.x[i].append(Var("x" + str(i) + str(j)))
        if self.state[i][j] == counter:
            self.E.add_constraint(self.x[i][j])
        else:
            self.E.add_constraint(~self.x[i][j])


    def __set_y_truth(self, i, j):
        """
        Sets the y truth values a given square in a grid

        @param grid_setup: 5x5 2-dimensional list of a grid state
        @type grid_setup: list of 5 lists of 5 Var objects
        @param i: row number of the square
        @type i: integer (1 <= i <= 3)
        @param j: column number of the square
        @type j: integer (1 <= j <= 3)
        """

        # This constant list is used to quickly get the coordinates of adjacent squares
        # The given square is in the middle, each adjacent square has the coordinates as shown:
        coordinates = [[i - 1, j - 1], [i - 1, j], [i - 1, j + 1],
                       [  i  , j - 1],             [  i  , j + 1],
                       [i + 1, j - 1], [i + 1, j], [i + 1, j + 1]]
        counter = 0  # Used for counting the number of adjacent mines or unknown squares

        for n in range(len(coordinates)):
            adjacent_square = self.state[coordinates[n][0]][coordinates[n][1]]
            # The following conditional checks if the nth adjacent square is a mine
            # or unknown
            if adjacent_square == -1 or adjacent_square == -2:
                counter += 1

        # Instantiates the y condition at the given coordinate and sets a constraint
        # for it
        self.y[i].append(Var("y" + str(i) + str(j)))
        if self.state[i][j] == counter:
            self.E.add_constraint(self.y[i][j])
        else:
            self.E.add_constraint(~self.y[i][j])


    def __set_truth_encodings(self):
        """
        Sets the constraints required to determine the state of the middle square
        """

        # If there are any adjacent squares with a True y condition, the middle square
        # is a mine. See the boolean condition guide (top) for an explanation
        self.E.add_constraint(iff((self.y[1][1] | self.y[1][2] | self.y[1][3] |
                                   self.y[2][1] | self.y[2][3] | self.y[3][1] |
                                   self.y[3][2] | self.y[3][3]), self.m[2][2]))
        # If there are any adjacent squares with a True x condition, the middle square
        # is safe. See the boolean condition guide (top) for an explanation
        self.E.add_constraint(iff((self.x[1][1] | self.x[1][2] | self.x[1][3] |
                                   self.x[2][1] | self.x[2][3] | self.x[3][1] |
                                   self.x[3][2] | self.x[3][3]), self.s[2][2]))
        # If the middle square isn't a mine or safe, it is unknown
        self.E.add_constraint(iff(~self.m[2][2] & ~self.s[2][2], self.u[2][2]))
    

    def get_solution(self, solution):
        """
        Returns the english representation of the solution

        @param solution: a solved 5x5 minesweeper model (using E.solve())
        @type solution: list of 5 lists of var objects
        @return 'schrodinger's mine': if the middle square is simultaneously a mine
                    and not a mine (you inputted an impossible state)
        @return 'mine': if the middle square is a mine
        @return 'safe': if the middle square is safe
        @return 'unknown': if the middle square is unknown
        @return an error message: if the grid could not be solved or an error occurred
                    (this should not happen, check constraints if you see this)
        @rtype: string
        """

        try:
            if solution['m22'] and solution['s22']:
                return "schrodinger's mine"
            if solution['m22']:
                return "mine"
            if solution['s22']:
                return "safe"
            return "unknown"
        except:
            return "error: key 'm22' or 's22' does not exist.\
                    Model is not satisfiable or an error occurred"


    def print_state(self):
        """
        Prints the minesweeper state similar to how it would look in a real game

        Prints a 'box' with each square being either a number (of adjacent mines),
        a question mark (unknown) or an M (mine). Also includes the state number

        @param state: a 5x5 minesweeper grid
        @type state: list of 5 lists of 5 var objects
        @param num: the state 'number'
        @type num: integer (either a pre-define state number or 'new')
        """
        grid_range = range(5)  # A range variable used to iterate through the grid

        print("\nSTATE %s:" % (str(self.state_num)))
        print("-----------")
        for i in grid_range:
            print('|', end='')
            for j in grid_range:
                square = self.state[i][j]
                if square == -2:
                    print('M', end='')
                elif square == -1:
                    print('?', end='')
                else:
                    print(str(square), end='')
                if j < len(self.state[i]) - 1:
                    print(" ", end='')
            print('|')
        print("-----------\n")