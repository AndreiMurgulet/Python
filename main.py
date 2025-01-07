"""
Module Name: main.py
Purpose: this module represents the entrance point of the game
"""
import sys
import tkinter as tk

from ui_welcome import MancalaWelcome


def main():
    if len(sys.argv) > 1:
        opponent_type = sys.argv[1]
    else:
        opponent_type = "human"

    root = tk.Tk()
    root.title("Mancala - Main")

    MancalaWelcome(root, opponent_type)
    root.mainloop()


if __name__ == "__main__":
    main()
