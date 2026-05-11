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
    p: set[int]
    
    def __init__(self, r, c, possibilities=None):
        self.row = r
        self.column = c
        self.block = ((r - 1) // 3) * 3 + ((c - 1) // 3) + 1

        if possibilities is None:
            possibilities = {1,2,3,4,5,6,7,8,9}

        self.p = set(possibilities)

        if len(self.p) == 0:
            raise ValueError("No possibilities here!")

        self.row_cells = None
        self.column_cells = None
        self.block_cells = None

    def is_solved(self) -> bool:
        return len(self.p) == 1

    def value(self) -> int:
        return next(iter(self.p))

    def __len__(self):
        return len(self.p)

    def __repr__(self):
        return str(self.p)

# the group contains cells
class House:
    def __init__(self, house_type, index):
        self.house_type = house_type
        self.index = index
        self.cells = []

    def add(self, cell):
        self.cells.append(cell)

    def remove(self, cell):
        self.cells.remove(cell)

    def __iter__(self):
        return iter(self.cells)

    def __len__(self):
        return len(self.cells)

    def __repr__(self):
        return f"{self.house_type} {self.index}"


# the class of Sudoku grid
# __init__ with multiline str
# function to show_stage_in_str
# function to show_stage_in_graphic
# function to show_progress_in_graphic
class Sudoku:

    grid: list[list[Cell]]
    unsolved: House

    def __init__(self, text: str):
        lines = text.strip().splitlines()

        self.rows = [House("Row", i) for i in range(9)]
        self.columns = [House("Column", i) for i in range(9)]
        self.blocks = [House("Block", i) for i in range(9)]

        self.grid = []
        self.unsolved = House("Unsolved", 0)

        for r, line in enumerate(lines):
            row = []
            for c, ch in enumerate(line):
                n = int(ch)
                if n == 0:
                    cell = Cell(r, c)
                    self.unsolved.add(cell)
                else:
                    cell = Cell(r, c, {n})

                # assign houses to the cell's attributes
                cell.row_cells = self.rows[r]
                cell.column_cells = self.columns[c]
                block_index = (r // 3) * 3 + (c // 3)
                cell.block_cells = self.blocks[block_index]

                # add cell into houses
                self.rows[r].add(cell)
                self.columns[c].add(cell)
                self.blocks[block_index].add(cell)

                row.append(cell)

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

                if cell.is_solved():
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
                if cell.is_solved():
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
                if cell.is_solved():
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
                        if n in cell.p:
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



    # prune in RCB: remove all the numbers occurs at 
    # the same row, column and block, for all cells
    # in unsolved list.
    # if any unsolved cell become solved then remove it
    # from unsolved cells and return true
    def prune_in_RCB(self):
        # index of newly solved cells
        newly_solved = []

        # for each unsolved cells
        for index, question_cell in enumerate(self.unsolved):
            
            # remove the number of solved cells from possibilities
            for cell in question_cell.row_cells:
                if cell.is_solved() and cell is not question_cell:
                    question_cell.p.discard(cell.value())

            for cell in question_cell.column_cells:
                if cell.is_solved() and cell is not question_cell:
                    question_cell.p.discard(cell.value())

            for cell in question_cell.block_cells:
                if cell.is_solved() and cell is not question_cell:
                    question_cell.p.discard(cell.value())

            # if the question_cell has newly solved then
            # save the index of newly solved cells
            if len(question_cell.p) == 1:
                newly_solved.append(question_cell)

        # remove solved cells from unsolved list
        for cell in newly_solved:
            self.unsolved.remove(cell)

        return bool(newly_solved)


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

# Process of solving
# instanciate a Sudoku
game = Sudoku(puzzle)

# show the initial state
# game.show_stage_in_graphic()

# 1st step: show all p
game.show_progress_in_graphic()

# 2nd step: prune in RCB
print(game.prune_in_RCB())
game.show_progress_in_graphic()
print(game.prune_in_RCB())
game.show_progress_in_graphic()
print(game.prune_in_RCB())
game.show_progress_in_graphic()
print(game.prune_in_RCB())
game.show_progress_in_graphic()
print(game.prune_in_RCB())
game.show_progress_in_graphic()
print(game.prune_in_RCB())
game.show_progress_in_graphic()


