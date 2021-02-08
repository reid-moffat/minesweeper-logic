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

# A class to represnt minesweeper states
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
    Prompts the user with the predefined states and tests the chosen state
    """

    # predefined_states has an expected result for each state
    num_states = len(predefined_states.state_list) // 2
    # Creates a list of all predefeind states as minesweeper state objects
    states = [state.MinesweeperState(predefined_states.state_list[2*i],
              predefined_states.state_list[2*i+1], i) for i in range(num_states)]

    # Prints out all of the predefined states
    print("Here the the predefined states:")
    for i in states:
        i.print_state()

    # Loops until the user chooses a valid state, then solves the state and prints out details
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
    unknown_state = [[-1 for i in range(5)] for i in range(5)]
    new_state = state.MinesweeperState(unknown_state)

    # Prints out some instructions for how to properly input states
    print("\n=====CUSTOM STATE CREATION=====")
    print("Enter states row by row, Each square separated by a space.")
    print("Center spot should be unknown (-1), this is what it is solving for.")
    print("Key:")
    print("-2: mine")
    print("-1: unknown")
    print("0 <= n <= 8: revealed number square with n adjacent mines")
    print("Ex. input: -1 -1 2 1 -2 (press enter to submit)")

    # Applies user inputted numbers to the state
    for row_num in range(5):
        # Print out intermediate state
        new_state.print_state()

        # Prompts the user to input a row, checks if it is valid and applies
        # it to the state if it is. If not, loop until a valid row is inputted
        while True:
            spot = input("Enter row %d: " % (row_num + 1))
            if re.match("^[0-9 ]+$", spot):  # Make sure all the inputs are numbers
                new_row = [int(x) for x in spot.split()]
                if len(new_row) == 5:  # Must have 5 values in the row
                    if all([i >= -2 and i <= 8 for i in new_row]):
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
