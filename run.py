"""
Queen's University - CISC 204
Course Modelling Project: Minesweeper solver
Submission date: December 6th, 2020

Formatting, documentation and general improvements done by
Reid Moffat after submission

@author Graham Carkner,
        Elliot Arbuthnot,
        Truman Be,
        Reid Moffat
"""

# A class to represent minesweeper states
import state

# Contains a list of constant states and their solutions (for testing)
import predefined_states

# Regex
import re


def main():
    """
    Prompts the user to decide if they want to use a predefined state
    or create their own, then solves the given state and outputs the result
    """

    # Loops until the user chooses to use a predefined state or make their own
    while True:
        choice = input("Would you like to use a predefined state (y/n)? ").strip().lower()
        if choice == 'y' or choice == 'n':
            break
        print("Invalid choice\n")

    if choice == 'y':
        use_predefined_state()
    else:
        make_mine_state()


def use_predefined_state():
    """
    Prompts the user to choose a predefined state (from predefined_states.py),
    solves it and prints the expected and model result
    """

    # predefined_states has an expected result for each state
    num_states = len(predefined_states.state_list) // 2
    # Creates a list of all predefined states as minesweeper state objects
    states = [state.MinesweeperState(predefined_states.state_list[2*i],
              predefined_states.state_list[2*i+1], i) for i in range(num_states)]

    # Prints out all of the predefined states
    print("Here the the predefined states:")
    for i in states:
        i.print_state()

    # Loops until a valid state is chosen, solves it and prints the result
    while True:
        state_num = input("Choose a state between 1 and %d: " % num_states).strip()
        if state_num.isnumeric():
            state_number = int(state_num)
            if 1 <= state_number <= num_states:
                states[state_number-1].test_state()
                break
            else:
                print("Invalid choice: enter an integer in the range [1, %d]\n" % num_states)
        else:
            print("Invalid choice: enter an integer\n")


def make_mine_state():
    """
    Creates and tests a new minesweeper state with user input
    """
    # Initializes a default state of all unknowns
    # This makes it easier to print out intermediary states
    unknown_state = [[-1 for i in range(5)] for i in range(5)]
    new_state = state.MinesweeperState(unknown_state)

    # Prints out some instructions for how to properly input states
    instructions = "\n=====CUSTOM STATE CREATION=====" \
                   "Enter states row by row, Each square separated by a space." \
                   "Center spot should be unknown (-1), this is what it is solving for." \
                   "Key:" \
                   "-2: mine" \
                   "-1: unknown" \
                   "0 <= n <= 8: revealed number square with n adjacent mines" \
                   "Ex. input: -1 -1 2 1 -2 (press enter to submit)"
    print(instructions)

    # Collects and applies user input to the unknown state
    for row_num in range(5):
        # Print out intermediate state
        new_state.print_state()

        # Prompts the user to input a row, checks if it is valid and applies
        # it to the state if it is. If not, prints out the issue and loops
        # until a valid row is inputted
        while True:
            spot = input("Enter row %d: " % (row_num + 1))
            # Checks if the input is just numbers (and spaces)
            if re.match("^[0-9 ]+$", spot):
                new_row = [int(x) for x in spot.split()]
                # Must have 5 values in the row
                if len(new_row) == 5:
                    # Each value must be a mine (-2), safe (-1) or revealed (0-8)
                    if all([-2 <= i <= 8 for i in new_row]):
                        new_state.set_row(new_row, row_num)
                        break
                    print("Each value must be in the range [-2, 8]\n")
                else:
                    print("5 values required, try again.\n")
            else:
                print("Invalid row, try again (only numbers allowed).\n")
        if row_num == 2:
            # The middle square is always unknown since the algorithm needs
            # to solve for it. The user can enter another value, but it is
            # automatically set to unknown
            new_state.set_square(-1, 2, 2)

    # Tests the new state
    new_state.test_state()


main()
