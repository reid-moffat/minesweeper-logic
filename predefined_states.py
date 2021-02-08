"""
Below are some initial 5x5 states that are used for testing the code
-Each 2-D list represents a minesweeper state
-Each integer element is a square on a 5x5 grid
-See '4th state example.PNG' for a real minesweeper state example

Notation explanation:
U: unknown square (middle square is always unknown because it is being solved for)
M: known mine (in a real game, this would be a flag)
0 <= n <= 8: uncovered spot with n adjacent bombs (includes diagonals)
"""

# Makes the states easier to understand, while still allowing for arithmetic
# comparisons to check the state
U = -1  # Unknown
M = -2  # Mine

state_list = [
    # State 1 is a mine
    [
        [1, U, U, U, U],
        [1, U, U, U, 2],
        [2, M, U, 3, 2],
        [3, M, 5, M, 1],
        [3, M, 3, 1, 1]
    ],
    "mine",

    # State 2 is a mine
    [
        [2, 1, 1, 2, M],
        [1, 2, U, U, U],
        [1, 3, U, 1, U],
        [1, M, U, U, 3],
        [1, 1, 2, 2, U]
    ],
    "mine",

    # State 3 is safe
    [
        [U, U, U, U, U],
        [U, U, 1, 0, U],
        [U, 1, U, 1, U],
        [U, 0, 1, M, U],
        [U, U, U, U, U]
    ],
    "safe",

    # State 4 is a mine
    [
        [1, 1, 1, 0, 0],
        [1, M, 2, 1, 0],
        [2, 3, U, 1, 0],
        [2, M, 3, 2, 1],
        [U, U, U, U, U]
    ],
    "mine",

    # State 5 is a mine
    [
        [1, 1, 1, 0, 0],
        [1, M, 2, 1, 0],
        [2, U, U, 1, 0],
        [U, U, U, 1, 0],
        [0, 0, 0, 0, 0]
    ],
    "mine",

    # State 6 is unknown
    [
        [U, U, U, U, U],
        [U, U, U, U, U],
        [U, U, U, U, U],
        [U, U, U, U, U],
        [U, U, U, U, U]
    ],
    "unknown",

    # State 7 is safe
    [
        [0, 0, 0, 0, 0],
        [0, U, M, 1, 0],
        [0, U, U, U, 0],
        [0, U, U, U, 0],
        [0, 0, 0, 0, 0]
    ],
    "safe",

    # State 8 is unknown
    [
        [U, U, 1, U, U],
        [U, 2, M, 2, U],
        [U, U, U, U, U],
        [U, 2, U, U, U],
        [U, U, U, U, U]
    ],
    "unknown",

    # State 9 is unknown
    [
        [1, 2, U, U, 2],
        [1, M, 3, 3, M],
        [1, 2, U, 2, 1],
        [1, 3, U, 3, 1],
        [1, M, M, M, 1]
    ],
    "unknown"
]
