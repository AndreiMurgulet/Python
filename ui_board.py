"""
Module Name: ui_welcome.py
Purpose: this module implements the interface for the Mancala Board
"""
import random
import tkinter as tk
import tkinter.messagebox as mb

from mancala_logic import MancalaGame


def calculate_pit_positions():
    """
    Setting the holding pots for each player
    Returns:
        - list of positions of each pit
    """
    positions = [(0, 0)] * 14
    start_x = 200
    spacing = 100
    y_bottom = 250
    for i in range(6):
        x = start_x + i * spacing
        positions[i] = (x, y_bottom)

    y_top = 150
    for i in range(6):
        pit_index = 12 - i
        x = start_x + i * spacing
        positions[pit_index] = (x, y_top)

    return positions


class MancalaBoard:
    """Class to initialize the board interface with the pits and seeds"""

    def __init__(self, root, opponent_type="human"):
        """
        Set up the table and the player type

        Parameters:
            -opponent_type (string): the type of opponent to play
        """
        self.root = root
        self.opponent_type = opponent_type
        self.root.title(f"Mancala vs {('Computer' if opponent_type == 'computer' else 'Player')}")

        self.canvas_width = 900
        self.canvas_height = 400

        self.canvas = tk.Canvas(
            root,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="teal"
        )
        self.canvas.pack()

        self.exit_button = tk.Button(root, text="Exit", command=self.root.quit, font=("Calibre", 14))
        self.exit_button.pack(pady=10)

        self.game = MancalaGame()

        self.store_top_oval = self.canvas.create_oval(
            10, 80,
            80, 320,
            fill="royalblue",
            outline="black",
            width=4
        )

        self.store_bottom_oval = self.canvas.create_oval(
            self.canvas_width - 80, 90,
            self.canvas_width - 10, 320,
            fill="royalblue",
            outline="black",
            width=4
        )

        self.pit_positions = calculate_pit_positions()
        self.pit_ids = [None] * 14
        self.draw_pits()
        self.draw_seeds()
        self.highlight_pits()

    def draw_pits(self):
        """Drawing the  12 pits"""
        radius = 40
        for i in range(14):
            if i in (6, 13):
                continue
            x, y = self.pit_positions[i]
            pit_id = self.canvas.create_oval(
                x - radius, y - radius,
                x + radius, y + radius,
                fill="lightgray", outline="black", width=2
            )
            self.pit_ids[i] = pit_id

            self.canvas.tag_bind(pit_id, "<Button-1>", lambda e, idx=i: self.handle_pit_click(idx))

    def draw_seeds(self):
        """Drawing the seeds"""
        self.canvas.delete("seed")
        for pit_index, count in enumerate(self.game.board):
            if count <= 0:
                continue

            if pit_index == 6:
                left, right = self.canvas_width - 80, self.canvas_width - 10
                top, bottom = 90, 320
                self.draw_store_seeds(count, left, right, top, bottom)

            elif pit_index == 13:
                left, right = 10, 80
                top, bottom = 80, 320
                self.draw_store_seeds(count, left, right, top, bottom)

            else:
                x_center, y_center = self.pit_positions[pit_index]
                self.draw_pit_seeds(x_center, y_center, count)

    def draw_pit_seeds(self, x_center, y_center, count):
        """
        drawing the pit seeds
        Parameters:
            - x_center (int): the x coordinate of the center of the pit seed
            - y_center (int): the y coordinate of the center of the pit seed
            - count (int): the count of seeds
        """
        spacing = 10
        cols = 5
        offset = 18
        for i in range(count):
            row = i // cols
            col = i % cols
            px = x_center - offset + col * spacing
            py = y_center - offset + row * spacing
            self.canvas.create_oval(
                px, py, px + 8, py + 8,
                fill="black", outline="white", tags="seed"
            )

    def draw_store_seeds(self, count, left, right, top, bottom):
        """
        Drawing the seeds in the player's storage
        Parameters:
            - count (int): the count of seeds
            - left (int): the x coordinate of the left side of the seed
            - right (int): the x coordinate of the right side of the seed
            - top (int): the y coordinate of the top side of the seed
            - bottom (int): the y coordinate of the bottom side of the seed
        """
        height = bottom - top
        width = right - left

        cols = 3
        rows = 10
        spacing_x = (width - 20) // (cols + 1)
        spacing_y = (height - 20) // (rows + 1)

        for i in range(count):
            row = i // cols
            col = i % cols
            px = (left + 25) + col * spacing_x
            py = (top + 10) + row * spacing_y

            self.canvas.create_oval(
                px - 4, py - 4, px + 4, py + 4,
                fill="black", outline="white", tags="seed"
            )

    def handle_pit_click(self, pit_index):
        """
        Makes the moves+checks the game state
        Parameters:
            - pit_index (int): the index of what the pit in which you need to draw
        """
        extra_turn = self.game.make_move(pit_index)
        self.draw_seeds()
        if self.game.check_game_end():
            self.end_game()
            return
        self.highlight_pits()
        if not extra_turn and self.opponent_type == "computer" and self.game.current_player == 2:
            self.root.after(1000, self.computer_move)

    def computer_move(self):
        """The computer chooses the next move."""
        valid_pits = [i for i in range(7, 13) if self.game.board[i] > 0]
        if not valid_pits:
            if self.game.check_game_end():
                self.end_game()
            return
        pit_chosen = random.choice(valid_pits)
        extra_turn = self.game.make_move(pit_chosen)
        self.draw_seeds()

        if self.game.check_game_end():
            self.end_game()
            return
        self.highlight_pits()

        if extra_turn and self.game.current_player == 2:
            self.root.after(1000, self.computer_move)

    def highlight_pits(self):
        """Highlights what pits you can pick"""
        for i in range(14):
            if i == 6 or i == 13:
                continue
            self.canvas.itemconfig(self.pit_ids[i], outline="black", width=2)

        if self.game.current_player == 1:
            pits_highlight = range(0, 6)
        else:
            pits_highlight = range(7, 13)

        for i in pits_highlight:
            self.canvas.itemconfig(self.pit_ids[i], outline="gold", width=4)

    def end_game(self):
        """ Display's the winner"""
        w = self.game.winner()
        if w == 1:
            msg = f"Player 1 wins! Score= {self.game.board[6]} vs {self.game.board[13]}"
        elif w == 2:
            msg = f"Player 2 wins! Score= {self.game.board[13]} vs {self.game.board[6]}"
        else:
            msg = f"Tie! {self.game.board[6]} vs {self.game.board[13]}"
        mb.showinfo("Game Over", msg)
