from game import Game  # Import backend Game class
import math
import copy
import numpy as np
class TicTacToe:
    def __init__(self):
        self.row_count = 3
        self.column_count = 3
        self.action_size = self.row_count * self.column_count

    def __repr__(self):
        return "TicTacToe"

    # TODO: Initialize state object
    # Backend, we have a state class and node's are objects of that class
    def get_initial_state(self):
        return np.zeros((self.row_count, self.column_count))
        # return State()

    # TODO: Change so that action (either from-to bitboard(s) or decoded from-to numbers & piece type) can be used to get next state
    def get_next_state(self, state, action, player):
        row = action // self.column_count
        column = action % self.column_count
        state[row, column] = player
        return state

    # TODO: Major discussion point
    def get_valid_moves(self, state):
        return (state.reshape(-1) == 0).astype(np.uint8)

    # This function checks if the player who plays the action on the current board (state) wins the game right?

    # TODO: Leddon will handle this once Zach has work done, will have to pass in another parameter of the player
    # Description: Did the player who made the last move win?
    def check_win(self, state, action):
        # TODO: What would this look like if bitboards are used?
        if action == None:
            return False

        row = action // self.column_count
        column = action % self.column_count
        player = state[row, column]

        return (
                np.sum(state[row, :]) == player * self.column_count
                or np.sum(state[:, column]) == player * self.row_count
                or np.sum(np.diag(state)) == player * self.row_count
                or np.sum(np.diag(np.flip(state, axis=0))) == player * self.row_count
        )

    # I don't understand what the "get_value" here does. It's 1 if the action the player plays wins and 0 otherwise? Why is it tied to the "get_terminated" "function"
    # TODO: See check_win. Have a lot of thoughts on this one. Leddon and Zach to work closely on.
    def get_value_and_terminated(self, state, action):
        if self.check_win(state, action):
            return 1, True
        if np.sum(self.get_valid_moves(state)) == 0:
            return 0, True
        return 0, False

    def get_opponent(self, player):
        return -player

    def get_opponent_value(self, value):
        return -value

    # The state is represented as initially all 0's, then 1's in the places where the current player has moved (when they view the board) and -1's where the opponent has played correct?
    # This function is then used to flip the perspective of the board so that the opponent can view it from their perspective right?

    # TODO: Flip the perspective of white and black. White's bitboards become black's and vice versa, and all the repetition and other flags also switch
    def change_perspective(self, state, player):
        return state * player

    # N × N × (M T + L)
    # TODO: Take the states in the queue and add the "L" part. Encode as stacked np array's as seen below
    def get_encoded_state(self, state):
        encoded_state = np.stack(
            (state == -1, state == 0, state == 1)
        ).astype(np.float32)

        return encoded_state

    # TODO: Another thing to remember is that we have to make a queue to store the T long history of the past states and repetitions
    # Link to paper: https://arxiv.org/pdf/1712.01815


# TODO: Same as TicTacToe class, this is just another "game" class
class ConnectFour:
    def __init__(self):
        self.row_count = 6
        self.column_count = 7
        self.action_size = self.column_count
        self.in_a_row = 4

    def __repr__(self):
        return "ConnectFour"

    def get_initial_state(self):
        return np.zeros((self.row_count, self.column_count))

    def get_next_state(self, state, action, player):
        row = np.max(np.where(state[:, action] == 0))
        state[row, action] = player
        return state

    def get_valid_moves(self, state):
        return (state[0] == 0).astype(np.uint8)

    def check_win(self, state, action):
        if action == None:
            return False

        row = np.min(np.where(state[:, action] != 0))
        column = action
        player = state[row][column]

        def count(offset_row, offset_column):
            for i in range(1, self.in_a_row):
                r = row + offset_row * i
                c = action + offset_column * i
                if (
                        r < 0
                        or r >= self.row_count
                        or c < 0
                        or c >= self.column_count
                        or state[r][c] != player
                ):
                    return i - 1
            return self.in_a_row - 1

        return (
                count(1, 0) >= self.in_a_row - 1  # vertical
                or (count(0, 1) + count(0, -1)) >= self.in_a_row - 1  # horizontal
                or (count(1, 1) + count(-1, -1)) >= self.in_a_row - 1  # top left diagonal
                or (count(1, -1) + count(-1, 1)) >= self.in_a_row - 1  # top right diagonal
        )

    def get_value_and_terminated(self, state, action):
        if self.check_win(state, action):
            return 1, True
        if np.sum(self.get_valid_moves(state)) == 0:
            return 0, True
        return 0, False

    def get_opponent(self, player):
        return -player

    def get_opponent_value(self, value):
        return -value

    def change_perspective(self, state, player):
        return state * player

    def get_encoded_state(self, state):
        encoded_state = np.stack(
            (state == -1, state == 0, state == 1)
        ).astype(np.float32)

        return encoded_state