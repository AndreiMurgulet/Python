"""
Module Name: ui_welcome.py
Purpose: this module implements the interface for the Mancala Board
"""
import tkinter as tk

from mancala_logic import MancalaGame


class MancalaBoard:
    """Class to initialize the board interface with the pits and seeds"""

    def __init__(self, root, opponent_type="human"):
        """Set up the table and the player type"""
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

        self.exit_button = tk.Button(root, text="Exit", command=self.root.quit, font=("Calibri", 14))
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

        self.pit_positions = self.calculate_pit_positions()
        self.pit_ids = [None] * 14
        self.draw_pits()
        self.draw_seeds()

    def calculate_pit_positions(self):
        """Setting the holding pots for each player"""
        positions = [None] * 14
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

    def draw_pits(self):
        """Drawing the  12 pits"""
        radius = 40
        for i in range(14):
            if i in (6, 13):
                continue  # skip store
            x, y = self.pit_positions[i]
            pit_id = self.canvas.create_oval(
                x - radius, y - radius,
                x + radius, y + radius,
                fill="burlywood", outline="black", width=2
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
                self.draw_store_seeds(6, count, left, right, top, bottom)

            elif pit_index == 13:
                left, right = 10, 80
                top, bottom = 80, 320
                self.draw_store_seeds(13, count, left, right, top, bottom)

            else:
                x_center, y_center = self.pit_positions[pit_index]
                self.draw_pit_seeds(pit_index, x_center, y_center, count)

    def draw_pit_seeds(self, pit_index, x_center, y_center, count):
        """drawing the pit seeds"""
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

    def draw_store_seeds(self, pit_index, count, left, right, top, bottom):
        """Drawing the seeds in the player's storage"""
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

        extra_turn = self.game.make_move(pit_index)
        self.draw_seeds()







