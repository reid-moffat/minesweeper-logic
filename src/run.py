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

from state import MinesweeperState
from predefined_states import state_list
from re import match, sub


def main():
    """
    Prompts the user to decide if they want to use a predefined state
    or create their own, then solves the given state and outputs the result
    """

    # Loops until the user chooses to use a predefined state or make their own
    while True:
        choice = input("Would you like to use a predefined state (y/n)? ").strip().lower()
        if choice in ['y', 'n']:
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

    # Creates a list of all predefined states as minesweeper state objects
    num_states = len(state_list)
    states = [MinesweeperState(state_list[i]['state'], state_list[i]['solution'], i) for i in state_list]

    # Prints out all of the predefined states
    print("Here the the predefined states:")
    for i in states:
        i.print_state()

    # Loops until a valid state is chosen, solves it and prints the result
    while True:
        state_num = input(f"Choose a state between 1 and {num_states}: ").strip()
        if state_num.isnumeric() and 1 <= int(state_num) <= num_states:
            states[int(state_num) - 1].test_state()
            break
        else:
            print(f"Invalid choice: enter an integer in the range [1, {num_states}]\n")


def make_mine_state():
    """
    Creates and tests a new minesweeper state with user input
    """
    # Initializes a default state of all unknowns
    # This makes it easier to print out intermediary states
    unknown_state = [[-1] * 5] * 5
    new_state = MinesweeperState(unknown_state)

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
        new_state.print_state()  # Print out intermediate state

        # Prompts the user to input a row, checks if it is valid and applies
        # it to the state if it is. If not, prints out the issue and loops
        # until a valid row is inputted
        while True:
            spot = sub(r'\s+', ' ', input(f"Enter row {row_num + 1}: ").strip())
            if match("^((-1|-2|[0-8]) ){4}(-1|-2|[0-8])$", spot):
                new_state.set_row(row_num, [int(x) for x in spot.split()])
                break
            else:
                print("Invalid row, must have 5 numbers in the range [-2, 8]\n")
        if row_num == 2:
            # The middle square is always unknown since the algorithm needs
            # to solve for it. The user can enter another value, but it is
            # automatically set to unknown
            new_state.set_square(2, 2, -1)

    new_state.test_state()


main()
