import tkinter as tk
from tkinter import messagebox
import random
from cell import Cell


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
