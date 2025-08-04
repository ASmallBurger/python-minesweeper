from board import Minesweeper

if __name__ == "__main__":
    # Change size/mines here for difficulty!
    app = Minesweeper(size=9, mines=10)
    app.mainloop()