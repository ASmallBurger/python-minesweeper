import tkinter as tk
from tkinter import messagebox

class Cell(tk.Button):
    COLORS = {
        1: "blue",
        2: "green",
        3: "red",
        4: "purple",
        5: "maroon",
        6: "turquoise",
        7: "black",
        8: "gray",

    }

    def __init__(self, master, x, y, game):
        super().__init__(
            master,
            width=2, height=1,
            font=("Arial", 13, "bold"),
            bg="#d3d3d3",  # grey for unrevealed
            relief="raised",
            borderwidth=2,
            highlightthickness=0
        )
        self.x, self.y = x, y
        self.game = game
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0

        # Mouse bindings
        self.bind("<Button-1>", self.on_left_click)
        self.bind("<Button-3>", self.on_right_click)
        self.bind("<Shift-Button-1>", self.on_shift_left_click)

    def on_left_click(self, event):
        if not self.is_flagged:
            self.game.reveal_cell(self.x, self.y)

    def on_right_click(self, event):
        if not self.is_revealed:
            self.toggle_flag()

    def on_shift_left_click(self, event):
        if not self.is_revealed:
            self.toggle_flag()

    def toggle_flag(self):
        if self.is_revealed:
            return
        # Placing a flag
        if not self.is_flagged:
            if self.game.flags_left == 0:
                return  # Prevent placing more flags than available
            self.is_flagged = True
            self.config(text="F", fg="red", bg="yellow")
            self.game.flags_left -= 1
        # Removing a flag
        else:
            self.is_flagged = False
            self.config(text="", fg="black", bg="#d3d3d3")
            self.game.flags_left += 1
        self.game.flag_label.config(text=f"Flags: {self.game.flags_left}")

    def reveal(self):
        if self.is_revealed:
            return
        self.is_revealed = True
        self.config(
            relief="sunken",
            state="disabled",
            bg="#bbbbbb"
        )
        if self.is_mine:
            self.config(
                text="*", fg="white", bg="red", disabledforeground="white"
            )
        elif self.neighbor_mines > 0:
            fg = self.COLORS.get(self.neighbor_mines, "black")
            self.config(
                text=str(self.neighbor_mines),
                disabledforeground=fg  # Use this for color!
            )
        else:
            self.config(text="")

    def show_mine(self):
        # Reveals a mine at Game Over
        self.config(
            text="*", fg="white", bg="red",
            relief="sunken", state="disabled", disabledforeground="white"
        )