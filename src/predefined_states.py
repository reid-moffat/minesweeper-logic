"""
Below are some initial 5x5 states that are used for testing the code
-Each 2-D list represents a minesweeper state
-Each integer element is a square on a 5x5 grid
-See '4th state example.PNG' for a real minesweeper state example

Notation explanation:
U: unknown square (middle square is always unknown because it is being solved for)
M: known mine (in a real game, this would be a flag)
0 <= n <= 8: uncovered spot with n adjacent bombs (includes diagonals)

To access a state, use state_list[n]['state'] where is is the state number
To access its solution, use state_list[n]['solution']
"""

# Makes states easier to understand visually by removing magic numbers
U = -1  # Unknown
M = -2  # Mine

state_list = {
    1: {
        'state': [
            [1, U, U, U, U],
            [1, U, U, U, 2],
            [2, M, U, 3, 2],
            [3, M, 5, M, 1],
            [3, M, 3, 1, 1]
        ],
        'solution': "mine"
    },

    2: {
        'state': [
            [2, 1, 1, 2, M],
            [1, 2, U, U, U],
            [1, 3, U, 1, U],
            [1, M, U, U, 3],
            [1, 1, 2, 2, U]
        ],

        'solution': "mine"
    },

    3: {
        'state': [
            [U, U, U, U, U],
            [U, U, 1, 0, U],
            [U, 1, U, 1, U],
            [U, 0, 1, M, U],
            [U, U, U, U, U]
        ],
        'solution': "safe"
    },

    4: {
        'state': [
            [1, 1, 1, 0, 0],
            [1, M, 2, 1, 0],
            [2, 3, U, 1, 0],
            [2, M, 3, 2, 1],
            [U, U, U, U, U]
        ],
        'solution': "mine"
    },

    5: {
        'state': [
            [1, 1, 1, 0, 0],
            [1, M, 2, 1, 0],
            [2, U, U, 1, 0],
            [U, U, U, 1, 0],
            [0, 0, 0, 0, 0]
        ],
        'solution': "mine"
    },

    6: {
        'state': [
            [U, U, U, U, U],
            [U, U, U, U, U],
            [U, U, U, U, U],
            [U, U, U, U, U],
            [U, U, U, U, U]
        ],
        'solution': "unknown"
    },

    7: {
        'state': [
            [0, 0, 0, 0, 0],
            [0, U, M, 1, 0],
            [0, U, U, U, 0],
            [0, U, U, U, 0],
            [0, 0, 0, 0, 0]
        ],
        'solution': "safe",
    },

    8: {
        'state': [
            [U, U, 1, U, U],
            [U, 2, M, 2, U],
            [U, U, U, U, U],
            [U, 2, U, U, U],
            [U, U, U, U, U]
        ],
        'solution': "unknown",
    },

    9: {
        'state': [
            [1, 2, U, U, 2],
            [1, M, 3, 3, M],
            [1, 2, U, 2, 1],
            [1, 3, U, 3, 1],
            [1, M, M, M, 1]
        ],
        'solution': "unknown"
    }
}
