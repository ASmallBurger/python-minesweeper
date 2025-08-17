import tkinter as tk
from tkinter import messagebox
import random
from cell import Cell


class Minesweeper(tk.Frame):
    def __init__(self, master, size=8, mines=10, on_home=None):
        super().__init__(master)
        self.on_home = on_home
        self.configure(bg="#e0e0e0")
        self.size = size
        self.mines = mines
        self.grid_cells = [[None for _ in range(size)] for _ in range(size)]
        self.mines_locations = set()
        self.game_over_flag = False
        top_controls = tk.Frame(self, bg="#e0e0e0")
        top_controls.grid(row=0, column=0, columnspan=size, sticky="we", pady=(5,10))
        self.create_widgets()
        self.place_mines()
        self.calculate_numbers()
        self.timer_label = tk.Label(top_controls, text="Time: 0", font=("Arial", 13, "bold"),
                                   bg="#e0e0e0", anchor="e", width=10)
        self.timer_label.pack(side="right", padx=10)

        self.elapsed_time = 0
        self.timer_running = False
        self.after_id = None
        self.start_timer()


        self.restart_button = tk.Button(
            top_controls, text="Restart", font=("Arial", 10, "bold"), width=7,
            command=self.restart_game, padx=2, pady=2
        )
        self.restart_button.pack(side="left", padx=4)

        self.home_button = tk.Button(
            top_controls, text="Home", font=("Arial", 10, "bold"), width=7,
            command=self.go_home, padx=2, pady=2
        )
        self.home_button.pack(side="left", padx=4)

        self.flags_left = mines
        self.flag_label = tk.Label(
            self, text=f"Flags: {self.flags_left}",
            font=("Arial", 13, "bold"), bg="#e0e0e0"
        )
        self.flag_label.grid(row=1, column=0, columnspan=size, pady=(0, 10))




        self.status_label = tk.Label(
            self, text="", font=("Arial", 13, "bold"),
            bg="#e0e0e0", fg="red"
        )
        self.status_label.grid(row=size+2, column=0, columnspan=size, pady=(10, 0))

    def create_widgets(self):
        for x in range(self.size):
            for y in range(self.size):
                cell = Cell(self, x, y, self)
                cell.grid(row=x + 2, column=y, padx=1, pady=1)
                self.grid_cells[x][y] = cell


    def go_home(self):
        self.destroy()
        if self.on_home:
            self.on_home()

    def place_mines(self):
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

    def start_timer(self):
        self.timer_running = True
        self.elapsed_time = 0
        self.update_timer()

    def update_timer(self):
        if self.timer_running:
            mins, secs = divmod(self.elapsed_time, 60)
            self.timer_label.config(text=f"Time: {mins:02}:{secs:02}")
            self.elapsed_time += 1
            self.after_id = self.after(1000, self.update_timer)

    def stop_timer(self):
        self.timer_running = False
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

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
            self.status_label.config(text="You clicked on a mine!")
            self.stop_timer()
            return

        if cell.neighbor_mines == 0:
            # Recursively reveal neighbors
            for i in range(max(0, x - 1), min(self.size, x + 2)):
                for j in range(max(0, y - 1), min(self.size, y + 2)):
                    if not self.grid_cells[i][j].is_revealed:
                        self.reveal_cell(i, j)

        self.check_win()

    def restart_game(self):

        self.status_label.config(text="", fg="red")
        for row in self.grid_cells:
            for cell in row:
                cell.destroy()

        self.grid_cells = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.mines_locations = set()
        self.game_over_flag = False

        self.flags_left = self.mines
        self.flag_label.config(text=f"Flags: {self.flags_left}")

        self.stop_timer()
        self.timer_label.config(text="Time: 0")
        self.start_timer()


        self.create_widgets()
        self.place_mines()
        self.calculate_numbers()




    def show_all_mines(self):
        for (x, y) in self.mines_locations:
            self.grid_cells[x][y].show_mine()
        self.disable_all_cells()

    def check_win(self):
        # Win if all non-mine cells are revealed
        for x in range(self.size):
            for y in range(self.size):
                cell = self.grid_cells[x][y]
                if not cell.is_mine and not cell.is_revealed:
                    return
        self.game_over_flag = True
        self.status_label.config(text="Congratulations! You won!", fg="green")
        self.disable_all_cells()
        self.stop_timer()

    def disable_all_cells(self):
        for row in self.grid_cells:
            for cell in row:
                cell.config(state='disabled')
