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

state_list = [
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