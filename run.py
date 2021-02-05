"""
Queen's University - CISC 204
Course Modelling Project: Minesweeper solver
Submission date: December 6th, 2020

Formatting and documentation improvements done by
Reid Moffat after submission

@author Graham Carkner,
        Elliot Arbuthnot,
        Truman Be,
        Reid Moffat
"""

import state

'''
Below are some initial 5x5 states that are used for testing the code
-Each 2-D list represents a minesweeper state
-Each integer element is a square on a 5x5 grid
-See '4th state example.PNG' for a real minesweeper state example

Notation explanation:
u: unknown square (middle square is always -1 because it is being solved for)
m: known mine (in a real game, this would be a flag)
0 <= n <= 8: uncovered spot with n adjacent bombs (includes diagonals)
'''

# TODO: replace all -1s with u and -2s with m in the states

# Makes the states easier to understand, while still allowing for arithmetic
# comparisons to check the state
u = -1
m = -2

predefined_states = [
    # State 1 is a mine
    [
        [1, -1, -1, -1, -1],
        [1, -1, -1, -1, 2],
        [2, -2, -1, 3, 2],
        [3, -2, 5, -2, 1],
        [3, -2, 3, 1, 1]
    ],
    "mine",

    # State 2 is a mine
    [
        [2, 1, 1, 2, -2],
        [1, 2, -1, -1, -1],
        [1, 3, -1, 1, -1],
        [1, -2, -1, -1, 3],
        [1, 1, 2, 2, -1]
    ],
    "mine",

    # State 3 is safe
    [
        [-1, -1, -1, -1, -1],
        [-1, -1, 1, 0, -1],
        [-1, 1, -1, 1, -1],
        [-1, 0, 1, -2, -1],
        [-1, -1, -1, -1, -1]
    ],
    "safe",

    # State 4 is a mine
    [
        [1, 1, 1, 0, 0],
        [1, -2, 2, 1, 0],
        [2, 3, -1, 1, 0],
        [2, -2, 3, 2, 1],
        [-1, -1, -1, -1, -1]
    ],
    "mine",

    # State 5 is a mine
    [
        [1, 1, 1, 0, 0],
        [1, -2, 2, 1, 0],
        [2, -1, -1, 1, 0],
        [-1, -1, -1, 1, 0],
        [0, 0, 0, 0, 0]
    ],
    "mine",

    # State 6 is unknown
    [
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1]
    ],
    "unknown",

    # State 7 is safe
    [
        [0, 0, 0, 0, 0],
        [0, -1, -2, 1, 0],
        [0, -1, -1, -1, 0],
        [0, -1, -1, -1, 0],
        [0, 0, 0, 0, 0]
    ],
    "safe",

    # State 8 is unknown
    [
        [-1, -1, 1, -1, -1],
        [-1, 2, -2, 2, -1],
        [-1, -1, -1, -1, -1],
        [-1, 2, -1, -1, -1],
        [-1, -1, -1, -1, -1]
    ],
    "unknown",

    # State 9 is unknown
    [
        [1, 2, -1, -1, 2],
        [1, -2, 3, 3, -2],
        [1, 2, -1, 2, 1],
        [1, 3, -1, 3, 1],
        [1, -2, -2, -2, 1]
    ],
    "unknown"
]


def main():
    """
    Prompts the user to decide if they want to use a predefined state
    or create their own, then solves the given state and outputs the result
    """

    # Loops until the user chooses to use a predefined state or make their own
    while True:
        choice = input("Would you like to use a predefined state? (y/n)? ")
        choice.strip().lower()
        if choice == 'y' or choice == 'n':
            break
        else:
            print("Invalid choice\n")

    if choice == 'y':
        use_pre_defined_state()
    else:
        make_mine_state()


def use_pre_defined_state():
    """
    Prompts the user with the predefined states and tests the chosen state
    """
    
    num_states = len(predefined_states) // 2
    states = [state.MinesweeperState(predefined_states[2*i], predefined_states[2*i+1], i)
              for i in range(num_states)]

    print("Here the the predefined states:")
    for i in states:
        i.print_state()
    
    while True:
        state_number = input("Choose a state between 1 and %d: " % num_states).strip()
        if state_number.isnumeric():
            state_number = int(state_number)
            if 1 <= state_number <= num_states:
                states[state_number-1].test_state()
                break
            else:
                print("Invalid choice\n")
        else:
            print("Invalid choice\n")


def make_mine_state():
    """
    Creates a new minesweeper state with user input
    """
    # Initializes a default state of all unknowns
    # This makes it easier to print out intermediary states
    unknown_state = [
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1]
    ]
    new_state = state.MinesweeperState(unknown_state)

    # Prints out some instructions for how to properly input states
    print("\n=====CUSTOM STATE CREATION=====")
    print("Enter states row by row, Each square separated by a space.")
    print("Ex. input: -1 -1 2 1 -2")
    print("Center spot should be unknown (-1), this is what it is solving for.")
    print("Key:")
    print("-2: mine")
    print("-1: unknown")
    print("0 <= n <= 8: revealed number square with n adjacent mines")

    # Applies user inputted numbers to the state
    for i in range(5):
        # Print out intermediate state
        new_state.print_state()

        # Prompts the user to input a row, checks if it is valid and applies
        # it to the state if it is. If not, loop until a valid row is inputted
        while True:
            spot = input("Enter row %d: " % (i + 1))
            try:  # Make sure all the inputs are numbers
                new_row = [int(x) for x in spot.split()]
                if len(new_row) == 5:  # Must have 5 values in the row
                    valid_row = True
                    for x in new_row:
                        if not (-2 <= x <= 8):  # Each value must be valid
                            print("Each value must be in the range [-2, 8]\n")
                            valid_row = False
                    if valid_row:
                        new_state.set_row(new_row, i)
                        break
                else:
                    print("5 values required, try again.\n")
            except ValueError:
                print("Invalid row, try again.\n")
        if i == 2:
            # The middle square is always unknown since the algorithm needs
            # to solve for it. Allowing another value to the middle won't
            # break the encoding, but it can be confusing
            new_state.set_square(-1, 2, 2)

    # If the user creates their own state, it is added to the list of states
    # (for the duration of the program) and tested
    new_state.test_state()


main()
