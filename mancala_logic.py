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

    def valid_pit_for_current_player(self, pit_index):
        """Check if it is your mancala"""
        if self.current_player == 1:
            return 0 <= pit_index <= 5
        else:
            return 7 <= pit_index <= 12

    def make_move(self, pit_index):
        """ Moving seeds"""

        if not self.valid_pit_for_current_player(pit_index):
            print("This is not your pit.")
            return False

        seeds = self.board[pit_index]

        self.board[pit_index] = 0
        self.board[pit_index] = 0
        current_pos = pit_index
        self.current_player = self.opposite_player()
        while seeds > 0:
            current_pos = (current_pos + 1) % 14
            self.board[current_pos] += 1
            seeds -= 1

        return False





