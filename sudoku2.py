# Refactor of Sudoku.py, preparing for recursive reasonning

# To copy nested list
from copy import deepcopy

# To draw the Sudoku in graphic
import matplotlib.pyplot as plt

# Cell class
# init(r, c, ps=None)
# remove_p_in_cell(p)
class Cell:

    row_number: int
    column_number: int
    block_number: int
    possibilities: set[int]
    row: House
    column: House
    block: House

    # init with coordinates in grid and possibilities
    def __init__(self, r, c, ps=None):
        self.row_number = r
        self.column_number = c
        self.block_number = ((r - 1) // 3) * 3 + ((c - 1) // 3) + 1

        if ps is None:
            ps = {1,2,3,4,5,6,7,8,9}

        self.possibilities = set(ps)

        self.row = None
        self.column = None
        self.block = None

    def remove_p_in_cell(self, p):
        self.possibilities.discard(p)

        # Ensure there is at least 1 p for the cell
        if len(self.possibilities) == 0:
            message = "No p left for the cell r: " + str(self.row) + " c: " + str(self.column)
            raise ValueError(message)

    @property
    def is_solved(self) -> bool:
        return len(self.possibilities) == 1

    def value(self) -> int:
        return next(iter(self.possibilities))

    def __len__(self):
        return len(self.possibilities)

    def __repr__(self):
        return str(self.possibilities)


# The group contains cells
# init(housse_type, index)
# add(cell)
# remove(cell)
# remove_p_in_house(p, exceptions)
# find_cell_with_p(p)
class House:
    def __init__(self, house_type, index):
        self.house_type: str = house_type
        self.index: int = index
        self.cells: [Cell] = []

    def add(self, cell):
        self.cells.append(cell)

    def remove(self, cell):
        self.cells.remove(cell)

    # method: remove p from all unsolved cells' ps in a house
    # skip the exempted cells
    def remove_p_in_house(self, p, exceptions):
        for cell in self:
            if cell.is_solved or cell in exceptions:
                continue
            cell.remove_p_in_cell(p)

    def __iter__(self):
        return iter(self.cells)

    def __len__(self):
        return len(self.cells)

    def __repr__(self):
        return f"{self.house_type} {self.index}"

    # To find cells with p
    # if count is absent, return all the cells with p
    def find_cell_with_p(self, p):

        cells = []

        for cell in self:
            if not cell.is_solved:
                if p in cell.p:
                    cells.append(cell)

        return cells


# the class of Sudoku grid
# __init__ with multiline str
# validate_all_cells()
# show_progress_in_graphic(title, highlighted_cells, show_p=True)
class Sudoku:

    grid: list[list[Cell]]

    unsolved_cells: House
    possibility_count: int = 0

    setp: int

    def __init__(self, text: str):

        self.grid = []
        self.unsolved_cells = House("Unsolved", 0)
        self.step = 0

        # Instanciate RCB houses
        self.rows = [House("Row", i) for i in range(9)]
        self.columns = [House("Column", i) for i in range(9)]
        self.blocks = [House("Block", i) for i in range(9)]

        # Instanciate cells,
        lines = text.strip().splitlines()

        for r, line in enumerate(lines):
            row = []
            for c, ch in enumerate(line):
                p = int(ch)
                if p == 0:
                    cell = Cell(r, c)
                    self.unsolved_cells.add(cell)
                    self.possibility_count += 9
                else:
                    cell = Cell(r, c, {p})
                    self.possibility_count += 1

                # assign RCB houses to the cell's attributes
                cell.row = self.rows[r]
                cell.column = self.columns[c]
                block_index = (r // 3) * 3 + (c // 3)
                cell.block = self.blocks[block_index]

                # add cell into RCB houses
                self.rows[r].add(cell)
                self.columns[c].add(cell)
                self.blocks[block_index].add(cell)

                # add cell into grid
                row.append(cell)

            self.grid.append(row)

    # validate_all_cells
    # 1. based on current possibilities of cells update unsolved cells 
    # 2. update the possibility count
    def validate_all_cells(self):
        pc = 0
        for row in self.rows:
            for cell in row:
                pc += len(cell.possibilities)
                if cell.is_solved and cell in self.unsolved_cells:
                    self.unsolved_cells.remove(cell)
                if not cell.is_solved and not cell in self.unsolved_cells:
                    self.unsolved_cells.add(cell)
        self.possibility_count = pc

    @property
    def is_solved(self):
        return not self.unsolved_cells


    # Show progress in graphic with title and highlighted cells
    def show_progress_in_graphic(self, title, highlighted_cells=[], show_p=True):
        fig, ax = plt.subplots(figsize=(9, 9))
        fig.suptitle(title, fontsize=24)
        ax.set_title(
            f"Unsolved cells: {len(self.unsolved_cells)}\nTatol possibilities: {self.possibility_count - 81}",
            fontsize=14
        )
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
                if cell.is_solved:
                    ax.text(
                        x0 + 0.5,
                        y0 + 0.5,
                        str(cell.value()),
                        ha="center",
                        va="center",
                        fontsize=24
                    )
                # candidate numbers
                elif show_p:
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


# Reasonning process
def reasonning(game):

    # count all p before this round techniques
    p_count_before = game.possibility_count
    print(p_count_before)

    # Technique: Basic eliminations
    method, highlighted_cells = basic_elimination(game)
    
    # Validate all cells
    game.validate_all_cells()
    print(game.possibility_count)

    # count all p after this round techniques
    p_count_after = game.possibility_count
    print(p_count_after)

    # If the method makes progress
    if not p_count_after == p_count_before:

        game.step += 1

        # show the result
        title = "Step " + str(game.step) + " " + str(method) + " result"
        game.show_progress_in_graphic(title, highlighted_cells)

        # If is solved
        if game.is_solved:
            game.show_progress_in_graphic("Sudoku has been solved!")
            return
        else:
            reasonning(game)

    else:
        game.show_progress_in_graphic("Final state and need more techniques!")


# Solve method: Basic elimination
# remove all the numbers occurs at the same row,
# column and block, for all unsolved cells.
# This can remove ps and solve cells
def basic_elimination(game):
    # index of newly solved cells
    newly_solved = []
    p_removed = False

    # for each unsolved cells
    for index, question_cell in enumerate(game.unsolved_cells):

        # remove the number of solved cells from possibilities
        for cell in question_cell.row:
            if cell.is_solved:
                question_cell.remove_p_in_cell(cell.value())

        for cell in question_cell.column:
            if cell.is_solved:
                question_cell.remove_p_in_cell(cell.value())

        for cell in question_cell.block:
            if cell.is_solved:
                question_cell.remove_p_in_cell(cell.value())

    return ("Basic Elimination", [])


def main():
    # example of Sudoku in str
    # BE is OK
    puzzle1 = """
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

    # BE HS is OK
    puzzle2 = """
806000000
240305000
003006904
000029600
050000009
300000517
000807401
000000000
000014038
"""

    # BE HS is OK
    puzzle3 = """
000700540
300020000
704000960
008205000
090180000
400906187
000800004
000403070
000000050
"""

    # BE HS is OK
    puzzle4 = """
006008010
000650002
080912003
037001506
004700800
000029000
040006000
000370008
000000700
"""

    # BE HS NP
    puzzle5 = """
000079150
000100600
100406000
490000020
005000700
200000008
060000002
020040900
007001004
"""

    # BE HS
    puzzle6 = """
000000000
009801730
070630180
000204000
001900003
090080040
040000000
003009061
000006304
"""

    # BE HS
    puzzle7 = """
100007090
030020008
009600500
005300900
010080002
600004000
300000010
040000007
007000300
"""

    # BE XW HS is OK
    puzzle8 = """
000000000
000003085
001020000
000507000
004000100
090000000
500000073
002010000
000040009
"""

    # instanciate a Sudoku
    game = Sudoku(puzzle8)

    # show the initial state
    game.show_progress_in_graphic("Initial State", False)

    # show all the possibilities
    game.show_progress_in_graphic("All Possibilities")

    reasonning(game)

if __name__ == "__main__":
    main()
