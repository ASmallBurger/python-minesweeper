import tkinter as tk
from board import Minesweeper

class HomeScreen(tk.Frame):

    def __init__(self, master, launch_game):
        super().__init__(master)
        self.launch_game = launch_game
        tk.Label(self, text="MINESWEEPER", font=("Arial", 20, "bold")).pack(pady=15)
        self.difficulty = tk.StringVar(value="easy")
        tk.Radiobutton(self, text="Easy (9x9, 10 mines)", variable=self.difficulty, value="easy").pack(anchor="w")
        tk.Radiobutton(self, text="Medium (16x16, 40 mines)", variable=self.difficulty, value="medium").pack(anchor="w")
        tk.Radiobutton(self, text="Hard (20x20, 60 mines)", variable=self.difficulty, value="hard").pack(anchor="w")
        tk.Button(self, text="Play", font=("Arial", 14), command=self.on_play).pack(pady=20)
    def on_play(self):
        diff = self.difficulty.get()
        if diff == "easy":
            size, mines = 9, 10
        elif diff == "medium":
            size, mines = 16, 40
        else:
            size, mines = 20, 60
        self.launch_game(size, mines)

def run_app():
    root = tk.Tk()
    root.title("Minesweeper")

    def start_game(size, mines):
        for widget in root.winfo_children():
            widget.destroy()
        def go_home():
            for w in root.winfo_children():
                w.destroy()
            home = HomeScreen(root, start_game)
            home.pack(fill="both", expand=True)

        game = Minesweeper(master=root, size=size, mines=mines, on_home=go_home)
        game.pack()
    home = HomeScreen(root, start_game)
    home.pack()
    root.mainloop()
