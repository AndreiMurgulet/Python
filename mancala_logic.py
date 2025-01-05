"""
Module Name: mancala_logic.py
Purpose: This module contains the main rules for the Mancala game, the point calculator and the stone's distribution.
"""


class MancalaGame:
    """ Class to initialize and handle the Game of Mancala"""

    def __init__(self):
        """Initialize the first state of the game"""
        self.board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        self.current_player = 1

    def player_side_range(self, player):
        """Check what player is moving and from what pots """
        if player == 1:
            return range(0, 6)
        else:
            return range(7, 13)

    def opposite_player(self):
        """Remember the player's turn"""
        return 2 if self.current_player == 1 else 1

    def player_store_index(self, player):
        """Assign a mancala space to store points"""
        return 6 if player == 1 else 13

    def opposite_store_index(self):
        return self.player_store_index(self.opposite_player())

    def valid_pit_for_current_player(self, pit_index):
        """Check if it is your pit"""
        if self.current_player == 1:
            return 0 <= pit_index <= 5
        else:
            return 7 <= pit_index <= 12

    def make_move(self, pit_index):
        """
        The implementation for rules:
        -don't deposit seeds in the enemies mancala
        -if the last seed is placed in an empty spot on your side you capture the seeds on the opponent side
        -if the last seed lands in your mancala you get another move
        """
        if not self.valid_pit_for_current_player(pit_index):
            print("This is not your pit.")
            return False

        seeds = self.board[pit_index]
        if seeds == 0:
            print("Empty pit,nothing to move.")
            return False

        self.board[pit_index] = 0
        current_pos = pit_index
        player_store = self.player_store_index(self.current_player)
        opponent_store = self.opposite_store_index()

        while seeds > 0:
            current_pos = (current_pos + 1) % 14
            if current_pos == opponent_store:
                continue
            self.board[current_pos] += 1
            seeds -= 1

        if current_pos == player_store:
            print("The last seed landed in your Mancala.You gen another turn.")
            return True

        if (self.current_player == 1 and current_pos in range(0, 6)) or \
                (self.current_player == 2 and current_pos in range(7, 13)):
            if self.board[current_pos] == 1:
                opposite = 12 - current_pos
                captured = self.board[opposite]
                if captured > 0:
                    self.board[opposite] = 0
                    self.board[current_pos] = 0
                    self.board[player_store] += captured + 1
                    print(f"You got {captured} seeds + 1 from your pit {current_pos}")

        self.current_player = self.opposite_player()

        return False

    def check_game_end(self):
        """ Verifies if the end state is achieved"""
        side1_empty = all(self.board[i] == 0 for i in range(0, 6))
        side2_empty = all(self.board[i] == 0 for i in range(7, 13))

        return side1_empty or side2_empty

    def winner(self):
        """
        Compare the 2 scores and return the winner
        """
        store_player1 = self.board[6]
        store_player2 = self.board[13]

        if store_player1 > store_player2:
            return 1
        elif store_player2 > store_player1:
            return 2
        else:
            return 0




