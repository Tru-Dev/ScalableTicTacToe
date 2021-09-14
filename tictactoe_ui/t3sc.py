"""
t3sc: Tic Tac Toe Scalable
Game classes for scalable Tic Tac Toe game.
"""
from enum import Enum, auto

class TurnResult(Enum):
    """
    Descriptive enum for the result of a turn
    """
    SUCCESS = auto()
    FAILURE = auto()
    WINNER = auto()
    DRAW = auto()

class TicTacToeScalable:
    """
    Game class for a scalable Tic Tac Toe game, meant to be implemented in some way
    (console, UI such as tkinter, graphically such as pygame, etc)
    """

    def __init__(self, size: int) -> None:
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.size = size
        self._player = 1

    def current_turn(self) -> int:
        """
        Returns the current player.
        """
        return self._player

    def move(self, row: int, col: int) -> TurnResult:
        """
        Takes the zero-indexed row and column coordinates of the player's move,
        updates the board, checks if there is a winner, and toggles the player's turn.
        Returns SUCCESS if the board updated successfully
        (i.e. there was no piece already there and coordinates were in bounds),
        WINNER if there was a winner detected,
        DRAW if a draw was detected,
        and FAILURE if the board failed to update at all.
        """
        if 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] == 0:
            self.board[row][col] = self._player
            if self.wincheck() == self._player:
                return TurnResult.WINNER
            space_left = False
            for row in self.board:
                for col in row:
                    if col == 0:
                        space_left = True
                        break
                if space_left:
                    break
            if not space_left:
                return TurnResult.DRAW
            self._player = 1 if self._player == 2 else 2
            return TurnResult.SUCCESS
        return TurnResult.FAILURE

    # Modified from Part 2 of the original Tic Tac Toe project
    def wincheck(self) -> int:
        """
        Takes the tic-tac-toe board and checks to see who the winner is.
        Returns 0 for no winner, or the player who won (1 or 2).
        Boards that seem to have more than one winner may cause unpredictable behavior.
        Non-square boards may also cause unpredictable behavior.
        """
        # Check rows
        for i in range(self.size):
            result = True
            for j in range(self.size - 1):
                result = result and self.board[i][j] == self.board[i][j + 1] != 0
            if result:
                return self.board[i][0]

        # Check columns
        for i in range(self.size):
            result = True
            for j in range(self.size - 1):
                result = result and self.board[j][i] == self.board[j + 1][i] != 0
            if result:
                return self.board[0][i]

        # Check diagonals
        result = True
        for i in range(self.size - 1):
            result = result and self.board[i][i] == self.board[i + 1][i + 1] != 0
        if result:
            return self.board[0][0]
        result = True
        for i in range(self.size - 1):
            result = result and (
                self.board[self.size - 1 - i][i] == self.board[self.size - 2 - i][i + 1] != 0
            )
        if result:
            return self.board[self.size - 1][0]

        # By now, we've checked all possibilities, there is no winner
        return 0

# TESTING
# wincheck() test cases
# test_cases_3x3 = [
#     [ # P2 Wins
#         [2, 2, 2],
#         [1, 0, 1],
#         [1, 0, 0],
#     ],
#     [ # P2 Wins
#         [2, 2, 0],
#         [2, 1, 0],
#         [2, 1, 1],
#     ],
#     [ # P1 Wins
#         [1, 2, 0],
#         [2, 1, 0],
#         [2, 1, 1],
#     ],
#     [ # P1 Wins
#         [0, 1, 0],
#         [2, 1, 0],
#         [2, 1, 1],
#     ],
#     [ # No winner
#         [1, 2, 0],
#         [2, 0, 1],
#         [2, 1, 2],
#     ],
#     [ # No winner
#         [1, 2, 0],
#         [2, 1, 0],
#         [2, 1, 0],
#     ]
# ]

# test_cases_4x4 = [
#     [ # P2 Wins
#         [2, 2, 2, 2],
#         [1, 0, 1, 1],
#         [1, 0, 0, 0],
#         [0, 0, 0, 0],
#     ],
#     [ # P2 Wins
#         [2, 2, 0, 0],
#         [2, 1, 0, 0],
#         [2, 1, 1, 0],
#         [2, 0, 0, 1],

#     ],
#     [ # P1 Wins
#         [2, 2, 0, 1],
#         [2, 1, 1, 0],
#         [2, 1, 1, 0],
#         [1, 0, 0, 2],
#     ],
#     [ # P1 Wins
#         [0, 1, 0, 2],
#         [2, 1, 0, 0],
#         [2, 1, 1, 0],
#         [0, 1, 0, 0],
#     ],
#     [ # No winner
#         [1, 2, 0, 0],
#         [2, 0, 1, 2],
#         [2, 1, 2, 0],
#         [1, 0, 0, 0],
#     ],
#     [ # No winner
#         [1, 2, 0, 0],
#         [2, 1, 0, 0],
#         [2, 1, 0, 0],
#         [1, 2, 0, 0],
#     ]
# ]

# Test Scenario
# if __name__ == "__main__":
#     game = TicTacToeScalable(3)
#     print(game.current_turn(), game.move(0, 0))
#     print(game.current_turn(), game.move(0, 1))
#     print(game.current_turn(), game.move(1, 1))
#     print(game.current_turn(), game.move(2, 2))
#     print(game.current_turn(), game.move(1, 2))
#     print(game.current_turn(), game.move(0, 2))
#     print(game.current_turn(), game.move(2, 0))
#     print(game.current_turn(), game.move(1, 0))
#     print(game.current_turn(), game.move(2, 1))
#     print(game.board)
