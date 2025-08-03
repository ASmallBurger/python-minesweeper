import tkinter as tk
from tkinter import messagebox
import random


class Cell(tk.Button):
    COLORS = {
        1: "blue",
        2: "green",
        3: "red",
        4: "purple",
        5: "maroon",
        6: "turquoise",
        7: "black",
        8: "gray"
    }

    def __init__(self, master, x, y, game):
        super().__init__(
            master,
            width=4, height=2,
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
        self.is_flagged = not self.is_flagged
        if self.is_flagged:
            self.config(text="F", fg="red", bg="yellow")
        else:
            self.config(text="", fg="black", bg="#d3d3d3")

    def reveal(self):
        if self.is_revealed:
            return
        self.is_revealed = True
        self.config(
            relief="sunken",
            state="disabled",
            bg="#bbbbbb",  # slightly darker gray
            disabledforeground="black"
        )
        if self.is_mine:
            self.config(
                text="*", fg="white", bg="red", disabledforeground="white"
            )
        elif self.neighbor_mines > 0:
            fg = self.COLORS.get(self.neighbor_mines, "black")
            self.config(
                text=str(self.neighbor_mines), fg=fg
            )
        else:
            self.config(text="")

    def show_mine(self):
        # Reveals a mine at Game Over
        self.config(
            text="*", fg="white", bg="red",
            relief="sunken", state="disabled", disabledforeground="white"
        )


class Minesweeper(tk.Tk):
    def __init__(self, size=8, mines=10):
        super().__init__()
        self.title("Minesweeper")
        self.configure(bg="#e0e0e0")
        self.size = size
        self.mines = mines
        self.grid_cells = [[None for _ in range(size)] for _ in range(size)]
        self.mines_locations = set()
        self.game_over_flag = False

        self.create_widgets()
        self.place_mines()
        self.calculate_numbers()

    def create_widgets(self):
        for x in range(self.size):
            for y in range(self.size):
                cell = Cell(self, x, y, self)
                cell.grid(row=x, column=y, padx=1, pady=1)
                self.grid_cells[x][y] = cell

    def place_mines(self):
        # Random mine placement
        while len(self.mines_locations) < self.mines:
            x = random.randrange(self.size)
            y = random.randrange(self.size)
            cell = self.grid_cells[x][y]
            if not cell.is_mine:
                cell.is_mine = True
                self.mines_locations.add((x, y))

    def calculate_numbers(self):
        for x in range(self.size):
            for y in range(self.size):
                cell = self.grid_cells[x][y]
                if cell.is_mine:
                    cell.neighbor_mines = -1
                    continue
                count = 0
                for i in range(max(0, x - 1), min(self.size, x + 2)):
                    for j in range(max(0, y - 1), min(self.size, y + 2)):
                        if self.grid_cells[i][j].is_mine:
                            count += 1
                cell.neighbor_mines = count

    def reveal_cell(self, x, y):
        if self.game_over_flag:
            return

        cell = self.grid_cells[x][y]
        if cell.is_revealed or cell.is_flagged:
            return
        cell.reveal()

        if cell.is_mine:
            cell.show_mine()
            self.game_over_flag = True
            self.show_all_mines()
            messagebox.showinfo("Game Over", "You clicked on a mine!")
            return

        if cell.neighbor_mines == 0:
            # Recursively reveal neighbors
            for i in range(max(0, x - 1), min(self.size, x + 2)):
                for j in range(max(0, y - 1), min(self.size, y + 2)):
                    if not self.grid_cells[i][j].is_revealed:
                        self.reveal_cell(i, j)

        self.check_win()

    def show_all_mines(self):
        for (x, y) in self.mines_locations:
            self.grid_cells[x][y].show_mine()

    def check_win(self):
        # Win if all non-mine cells are revealed
        for x in range(self.size):
            for y in range(self.size):
                cell = self.grid_cells[x][y]
                if not cell.is_mine and not cell.is_revealed:
                    return
        self.game_over_flag = True
        messagebox.showinfo("Congratulations!", "You won!")


if __name__ == "__main__":
    # Change size/mines here for difficulty!
    app = Minesweeper(size=8, mines=10)
    app.mainloop()
