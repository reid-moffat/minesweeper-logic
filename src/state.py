"""
Minesweeper state class

Represents and solves a 5x5 minesweeper state
"""

from typing import List
from lib204 import Encoding
from nnf import Var
from nnf.operators import iff


class MinesweeperState:

    def __init__(self, new_state, expected_result=None, num=-1):

        self.state = new_state[:]  # 5x5 minesweeper state
        self.solution = None  # Model solution solved with an encoding
        self.expected = expected_result  # Only used with predefined states
        self.state_num = num  # Number for predefined states (-1 for custom)

        '''
        Boolean condition guide:

        Each of the following lists will contain the boolean values for a
        specified condition for each square on the 5x5 board. Every square 
        will be given a True or False value for each of these five conditions

        -x is a revealed spot where the number of adjacent mines is equal to
        the number of adjacent squares that we know are mines (x is 
        'satisfied'. This means that all of the adjacent unknown squares are
        safe)
            -This condition is used to check if the middle square is safe. We
            can only be sure of the safety of the middle square if there is 
            at least one adjacent x
        -y is a revealed spot where the number of adjacent mines is equal to
        the number of adjacent known mines and the number of adjacent 
        unrevealed squares (this means that every unknown square around a y 
        square is a mine)
            -This condition is used to check if the middle square is a mine.
            We can only be sure the middle square is a mine if there is at 
            least one adjacent y
        -m (mine) is a square that has not been revealed and we know it has a
        mine (a flag in a real game of minesweeper)
        -s (safe) is a square that has not been revealed and we know it does
        not have a mine (a square that you would click to reveal in a real 
        game of minesweeper)
        -u (unknown) is a square that has not been revealed and we don't know
        if it is amine or a safe spot

        Notes:
        -If a square is revealed, it can have 3 possible states:
            1. True x condition and False for every other condition
            2. True y condition and False for every other condition
            3. False for all conditions (the square is revealed but we aren't
            sure where all the adjacent mines are, i.e not an x or a y. For 
            example, a square with 2 adjacent mines but we only know where 
            one of them is)

            Important: It is not possible in our case to have a True x
            condition and a True y condition. This would occur if a square 
            is a satisfied x with no adjacent unknown squares; but this 
            won't happen because the middle square is unknown and we only 
            find x and y conditions for the inner ring of 8 squares

        -If a square is not revealed, it has to be one of the three revealed
        conditions:
            1. If we know the square is a mine, m is True and all other
               conditions are False
            2. If we know the square is safe, s is True and all other
               conditions are False
            3. If we don't know if the square is a mine or safe, u is True and
               all other conditions are False
        '''

        # x boolean condition for each square
        self.x = [[] for i in range(5)]

        # y boolean condition for each square
        self.y = [[] for i in range(5)]

        # mine boolean condition for each square
        self.m = [[] for i in range(5)]

        # unknown boolean condition for each square
        self.u = [[] for i in range(5)]

        # safe boolean condition for each square
        self.s = [[] for i in range(5)]

        self.E = Encoding()  # Encoding initialization used to solve this model

    def set_square(self, i: int, j: int, new_value: int):
        """
        Sets a specified square in this state to a specified value, raising an
        exception if a parameter is not in the correct range

        @param i: column number
        @param j: row number
        @param new_value: a new value for the square
        """
        if not isinstance(i, int) or not 0 <= i <= 4:
            raise Exception("error: column number must be an integer in the range [0, 4]")
        if not isinstance(j, int) or not 0 <= j <= 4:
            raise Exception("error: row number must be an integer in the range [0, 4]")
        if not isinstance(new_value, int) or not -2 <= new_value <= 8:
            raise Exception("error: new value must be an integer in the range [-2, 8]")
        self.state[i][j] = new_value

    def set_row(self, i: int, new_row: List):
        """
        Sets the specified row to a new row (values are copied), raising an exception
        if a parameter is not in the correct range

        @param i: row number
        @param new_row: the new row of squares
        """
        if not isinstance(i, int) or not 0 <= i <= 4:
            raise Exception("error: column number must be an integer in the range [0, 4]")
        if not isinstance(new_row, list) or len(new_row) != 5 \
                or not all([True if isinstance(square, int) and -2 <= square <= 8 else False for square in new_row]):
            raise Exception("error: new row must have 5 integers in the range [-2, 8]")
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
        self.solution = self.E.solve()  # Solves the encoding

        self.print_state()

        # Prints if the encoding is satisfiable, the expected result and model result
        print("SATISFIABLE: " + str(self.E.is_satisfiable()) + "\n")
        if self.expected:
            print("Expected result:", self.expected)
        print(f"Model result: {self.get_solution()}\n")

        if input("Would you like to see the full solution states ('y' to see)? ").strip().lower() == 'y':
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
                    print(keyu, self.solution[keyu])
                    print(keym, self.solution[keym])
                    print(keyx, self.solution[keyx])
                    print(keyy, self.solution[keyy])
                    if i == 2 and j == 2:
                        print("s22", self.solution["s22"])
                    print()

    def __create_encoding(self):
        """
        Sets up the grid with the required encodings
        """
        self.__set_initial_state()
        self.__set_truth_encodings()

    def __set_initial_state(self):
        """
        Sets the initial state of this minesweeper grid
        """
        grid_range = range(5)

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
                        raise Exception('error: each square of the grid must'
                                        'have a value between -2 and 8'
                                        f'inclusive. Square [{i}][{j}] has a'
                                        f'value of {state}')

                    self.E.add_constraint(self.m[i][j] if state == -2 else ~self.m[i][j])  # mine
                    self.E.add_constraint(self.u[i][j] if state == -1 else ~self.u[i][j])  # unknown
                    self.E.add_constraint(self.s[i][j] if state > -1 else ~self.s[i][j])  # revealed square

        # Initializing x and y cases for the center 3x3 grid
        for i in grid_range:
            for j in grid_range:
                if 0 < i < 4 and 0 < j < 4:
                    self.__set_x_truth(i, j)
                    self.__set_y_truth(i, j)
                else:
                    self.x[i].append(Var("x" + str(i) + str(j)))
                    self.y[i].append(Var("y" + str(i) + str(j)))

    def __set_x_truth(self, i: int, j: int):
        """
        Sets the x truth values a given square in a grid

        @param i: row number of the square
        @param j: column number of the square
        """

        # This constant list is used to quickly get the coordinates of adjacent squares
        coordinates = [[i - 1, j - 1], [i - 1, j], [i - 1, j + 1],
                       [i, j - 1], [i, j + 1],
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

    def __set_y_truth(self, i: int, j: int):
        """
        Sets the y truth values a given square in a grid

        @param i: row number of the square
        @param j: column number of the square
        """

        # This constant list is used to quickly get the coordinates of adjacent squares
        # The given square is in the middle, each adjacent square has the coordinates as shown:
        coordinates = [[i - 1, j - 1], [i - 1, j], [i - 1, j + 1],
                       [i, j - 1], [i, j + 1],
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

    def get_solution(self) -> str:
        """
        Returns the english representation of the solution

        @return 'schrodinger's mine': if the middle square is simultaneously a mine
                    and not a mine (you inputted an impossible state)
        @return 'mine': if the middle square is a mine
        @return 'safe': if the middle square is safe
        @return 'unknown': if the middle square is unknown
        @return an error message: if the grid could not be solved or an error occurred
                    (this should not happen, check constraints if you see this)
        """

        try:
            if self.solution['m22'] and self.solution['s22']:
                return "schrodinger's mine"
            if self.solution['m22']:
                return "mine"
            if self.solution['s22']:
                return "safe"
            return "unknown"
        except KeyError:
            return "error: key 'm22' or 's22' does not exist.\
                    Model is not satisfiable or an error occurred"

    def print_state(self):
        """
        Prints the minesweeper state similar to how it would look in a real game

        Prints a 'box' with each square being either a number (of adjacent mines),
        a question mark (unknown) or an M (mine). Also includes the state number
        """
        grid_range = range(5)

        print(f"\nSTATE {str(self.state_num)}:")
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
