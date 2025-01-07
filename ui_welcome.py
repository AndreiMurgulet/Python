"""
Module Name: ui_welcome.py
Purpose: this module implements the interface for the welcome screen
"""
import tkinter as tk
from PIL import Image, ImageTk
from PIL.Image import Resampling

from ui_board import MancalaBoard


class MancalaWelcome:
    """Class to initialize the welcome interface and start button"""

    def __init__(self, root, opponent_type="human"):
        """
        Initialize the game state and start button

        Parameters:
            -opponent_type (str): the type of opponent human or computer

        """
        self.root = root
        self.root.title("Mancala - Welcome Screen")
        self.opponent_type = opponent_type

        self.canvas_width = 900
        self.canvas_height = 400

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(fill="both", expand=True)

        self.bg_image = Image.open("Mancala_background.jpg")
        self.bg_image = self.bg_image.resize((self.canvas_width, self.canvas_height), Resampling.LANCZOS)
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)

        self.canvas.create_image(0, 0, image=self.bg_image_tk, anchor='nw')

        self.label = tk.Label(root, text="Welcome to the Game of Mancala!", font=("Calibre", 16))
        self.start_button = tk.Button(root, text="Start Game", font=("Calibre", 14), command=self.start_game)

        self.canvas.create_window(self.canvas_width / 2, 50, anchor="n", window=self.label)
        self.canvas.create_window(self.canvas_width / 2, 160, anchor="n", window=self.start_button)

    def start_game(self):
        """Begin the game"""
        self.canvas.destroy()
        MancalaBoard(self.root, self.opponent_type)
