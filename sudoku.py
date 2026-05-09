# to copy nested list
from copy import deepcopy

# to draw the Sudoku in graphic
import matplotlib.pyplot as plt

# the class of single cell:
# __init__ with the possibilities
# Cell.solved
# Cell.value
# Cell.len
# Cell.repr
class Cell:

    row: int
    column: int
    block: int
    possibilities: set[int]
    
    def __init__(self, row, column, possibilities=None):
        self.row = row
        self.column = column
        self.block = ((row - 1) // 3) * 3 + ((column - 1) // 3) + 1

        if possibilities is None:
            possibilities = {1,2,3,4,5,6,7,8,9}

        self.possibilities: set[int] = set(possibilities)

        if len(self.possibilities) == 0:
            raise ValueError("No possibilities here!")
        print(self.row, self.column, self.block)

    @property
    def solved(self) -> bool:
        return len(self.possibilities) == 1

    def value(self) -> int:
        return next(iter(self.possibilities))

    def __len__(self):
        return len(self.possibilities)

    def __repr__(self):
        return str(self.possibilities)

# the class of Sudoku grid
# __init__ with multiline str
# function to show_stage_in_str
# function to show_stage_in_graphic
# function to show_progress_in_graphic
class Sudoku:
    def __init__(self, text: str):
        lines = text.strip().splitlines()
        self.grid: list[list[Cell]] = []
        for r, line in enumerate(lines, start=1):
            row = []
            for c, ch in enumerate(line, start=1):
                n = int(ch)
                if n == 0:
                    row.append(Cell(r, c))
                else:
                    row.append(Cell(r, c, {n}))
            self.grid.append(row)

    def show_stage_in_str(self):
        # add edge
        print("-" * 25)
        for r, row in enumerate(self.grid):

            # horizontal separators
            if r in (3, 6):
                print("-" * 25)

            line = []

            # add edge
            line.append("|")

            for c, cell in enumerate(row):

                # vertical separators
                if c in (3, 6):
                    line.append("|")

                if cell.solved:
                    line.append(str(cell.value()))
                else:
                    line.append(".")

            # add edge
            line.append("|")

            print(" ".join(line))
        # add adge
        print("-" * 25)
        print("")


    def show_stage_in_graphic(self):
        fig, ax = plt.subplots(figsize=(6, 6))
        # grid lines
        for i in range(10):
            linewidth = 3 if i % 3 == 0 else 1
            # horizontal
            ax.plot([0, 9], [i, i], linewidth=linewidth)
            # vertical
            ax.plot([i, i], [0, 9], linewidth=linewidth)
        # numbers
        for r in range(9):
            for c in range(9):
                cell = self.grid[r][c]
                if cell.solved:
                    ax.text(
                        c + 0.5,
                        8.5 - r,
                        str(cell.value()),
                        ha="center",
                        va="center",
                        fontsize=20
                    )
        ax.set_xlim(0, 9)
        ax.set_ylim(0, 9)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect("equal")
        plt.show() 

    def show_progress_in_graphic(self):
        fig, ax = plt.subplots(figsize=(9, 9))
        # draw grid lines
        for i in range(10):
            linewidth = 3 if i % 3 == 0 else 1
            # horizontal
            ax.plot([0, 9], [i, i], color="black", linewidth=linewidth)
            # vertical
            ax.plot([i, i], [0, 9], color="black", linewidth=linewidth)
        # draw cells
        for r in range(9):
            for c in range(9):
                cell = self.grid[r][c]
                x0 = c
                y0 = 8 - r
                # solved cell
                if cell.solved:
                    ax.text(
                        x0 + 0.5,
                        y0 + 0.5,
                        str(cell.value()),
                        ha="center",
                        va="center",
                        fontsize=24
                    )
                # candidate numbers
                else:
                    for n in range(1, 10):
                        if n in cell.possibilities:
                            # mini-grid position
                            sub_r = (n - 1) // 3
                            sub_c = (n - 1) % 3
                            x = x0 + (sub_c + 0.5) / 3
                            y = y0 + 1 - (sub_r + 0.5) / 3
                            ax.text(
                                x,
                                y,
                                str(n),
                                ha="center",
                                va="center",
                                fontsize=8
                            )
        ax.set_xlim(0, 9)
        ax.set_ylim(0, 9)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect("equal")
        plt.show()

# example of Sudoku str
puzzle = """
530070000
600195000
098000060
800760003
400853001
700920006
060037284
000419605
000080079
"""

# instanciate a Sudoku
game = Sudoku(puzzle)

game.show_stage_in_graphic()

game.show_progress_in_graphic()
