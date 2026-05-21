# Refactor of Sudoku.py, preparing for recursive reasonning

# To copy nested list
from copy import deepcopy

# To draw the Sudoku in graphic
import matplotlib.pyplot as plt

# Cell class
# init(r, c, ps=None)
# remove_p_from_cell(p)
# solved
# value()
# len()
# repr()
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

    @property
    def solved(self) -> bool:
        return len(self.possibilities) == 1

    def value(self) -> int:
        return next(iter(self.possibilities))

    def __len__(self):
        return len(self.possibilities)

    def __repr__(self):
        return str(self.possibilities)

    def remove_p_from_cell(self, p):
        self.possibilities.discard(p)

        # Ensure there is at least 1 p for the cell
        if len(self.possibilities) == 0:
            message = "No " + str(p) + " left for the cell r: " + str(self.row) + " c: " + str(self.column) + str(self)
            raise ValueError(message)


# The group contains cells
# init(housse_type, index)
# add(cell)
# remove(cell)
# iter()
# len()
# repr()
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

    def __iter__(self):
        return iter(self.cells)

    def __len__(self):
        return len(self.cells)

    def __repr__(self):
        return f"{self.house_type} {self.index}"

    # method: remove p from all unsolved cells' ps in a house
    # skip the exempted cells
    def remove_p_in_house(self, p, exceptions):
        for cell in self:
            if cell.solved or cell in exceptions:
                continue
            cell.remove_p_from_cell(p)

    # To find cells with p
    # if count is absent, return all the cells with p
    def find_cell_with_p(self, p):

        cells = []

        for cell in self:
            if not cell.solved:
                if p in cell.possibilities:
                    cells.append(cell)

        return cells


# the class of Sudoku grid
# __init__ with multiline str
# is_solved()
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

    def is_solved(self):
        return not self.unsolved_cells

    # validate_all_cells
    # 1. based on current possibilities of cells update unsolved cells 
    # 2. update the possibility count
    def validate_all_cells(self):
        pc = 0
        for row in self.rows:
            for cell in row:
                pc += len(cell.possibilities)
                if cell.solved and cell in self.unsolved_cells:
                    self.unsolved_cells.remove(cell)
                if not cell.solved and not cell in self.unsolved_cells:
                    self.unsolved_cells.add(cell)
        self.possibility_count = pc

    # Show progress in graphic with title and highlighted cells
    def show_progress_in_graphic(self, title, highlighted_cells=[], show_p=True):
        fig, ax = plt.subplots(figsize=(9, 9))
        fig.suptitle(title, fontsize=24)
        ax.set_title(
            f"Unsolved cells: {len(self.unsolved_cells)}\nTatal possibilities: {self.possibility_count}",
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


# Solve method: Basic elimination
# remove all the numbers occurs at the same row,
# column and block, for all unsolved cells.
# This can remove ps and solve cells
def basic_elimination(game):

    removes_to_do = set()

    # for each unsolved cells
    for question_cell in game.unsolved_cells:

        peers = (
            set(question_cell.row)
            | set(question_cell.column)
            | set(question_cell.block)
        )

        for cell in peers:
            if cell.solved:
                removes_to_do.add((question_cell, cell.value()))

    # do the removes
    for q_c, c_v in removes_to_do:
        q_c.remove_p_from_cell(c_v)

    return ("Basic Elimination", [])


# Solve method: Hidden Singles
# This searcheshe hidden singles in all House class.
# This can solve cells
def hidden_single(game):

    newly_solved = []

    # search in all RCB
    for house in game.rows + game.columns + game.blocks:

        # count candidate occurrences
        number_occurrences = {}

        for i in range(1, 10):
            number_occurrences[i] = []

        # iterate all cells but solved ones
        for cell in house:
            if cell.solved:
                continue
            else:
                for p in cell.possibilities:
                    number_occurrences[p].append(cell)

        # hidden single check
        for number, cells in number_occurrences.items():
            if len(cells) == 1:
                target = cells[0]
                newly_solved.append((target, number))

    # solve the cells
    for cell, number in newly_solved:
        cell.possibilities = {number}

    return ("Hidden Single", [])


# Solve method: Naked Pairs
# This searchess naked pairs in all Houses.
# This can remove ps.
def naked_pair(game):

    # searching naked pairs in all houses
    # iterate all houses
    # find cells with the same possibilities set to get a pair
    # if the possibility count equals the cell count in the pair
    # remove the possibilities in the set from all the other cells in the house

    # search all houses
    for house in game.rows + game.columns + game.blocks:

        # dictionary:
        # key   -> possibility set
        # value -> cells having that set
        groups = {}

        # 1-4:
        # iterate cells
        # get unsolved cells
        # save p sets
        # group cells with same p set
        for cell in house:

            if cell.solved:
                continue

            key = frozenset(cell.possibilities)

            if key not in groups:
                groups[key] = []

            groups[key].append(cell)

        # 5:
        # naked subset check
        for p_set, cells in groups.items():

            possibility_count = len(p_set)
            cell_count = len(cells)

            # naked pair/triple/quad...
            if possibility_count == cell_count:

                # 6:
                # remove possibilities from other cells
                for other in house:

                    if other in cells:
                        continue

                    for p in p_set:

                        if p in other.possibilities:
                            other.possibilities.discard(p)

    return ("Naked Pair", [])


# Solve method: X_Wings
def x_wings(game):

    # 1. find 2 n in row or column houses
    for n in range(1, 10):

        # row section
        for row_number1 in range(0, 9):

            c12 = game.rows[row_number1].find_cell_with_p(n)

            if len(c12) == 2:

                c1, c2 = c12[0], c12[1]

                # 2. find 2 n in row2 at same places
                for row_number2 in range(row_number1 + 1, 9):

                    c34 = game.rows[row_number2].find_cell_with_p(n)

                    if len(c34) == 2:

                        c3, c4 = c34[0], c34[1]

                        if c1.column_number == c3.column_number and c2.column_number == c4.column_number:

                            # 3. remove n from the places' perpendicular houses' cells' p
                            game.columns[c1.column_number].remove_p_in_house(n, c12 + c34)
                            game.columns[c2.column_number].remove_p_in_house(n, c12 + c34)

        # column section
        for column_number1 in range(0, 9):

            c12 = game.columns[column_number1].find_cell_with_p(n)

            if len(c12) == 2:

                c1, c2 = c12[0], c12[1]

                # 2. find 2 n in 2 at same places
                for column_number2 in range(column_number1 + 1, 9):

                    c34 = game.columns[column_number2].find_cell_with_p(n)

                    if len(c34) == 2:

                        c3, c4 = c34[0], c34[1]

                        if c1.row_number == c3.row_number and c2.row_number == c4.row_number:

                            # 3. remove n from the places' perpendicular houses' cells' p
                            game.rows[c1.row_number].remove_p_in_house(n, c12 + c34)
                            game.rows[c2.row_number].remove_p_in_house(n, c12 + c34)

    return ("X Wing", [])


# Solve method: Pointing and claiming
# if all p of certain number locate one row or column in a block
# then remove the number from the other cells of the line
def pointing_and_claiming(game):

    # pointing
    # iteration numbers in iteration of blocks
    for block in game.blocks:

        for number in range(1, 10):

            cells = [c for c in block if number in c.possibilities]

            if not cells:
                continue

            # check same row
            rows = {c.row for c in cells}

            if len(rows) == 1:

                row = next(iter(rows))

                for cell in row:

                    if cell in block:
                        continue

                    if not cell.solved:
                        cell.remove_p_from_cell(number)

            # check same column
            columns = {c.column for c in cells}

            if len(columns) == 1:

                column = next(iter(columns))

                for cell in column:

                    if cell in block:
                        continue

                    if not cell.solved:
                        cell.remove_p_from_cell(number)

    # claiming
    # iteration numbers in iteration of rows and columns
    for house in game.rows + game.columns:

        for number in range(1, 10):

            cells = [c for c in house if number in c.possibilities]

            if not cells:
                continue

            # check same block
            blocks = {c.block for c in cells}

            if len(blocks) == 1:

                block = next(iter(blocks))

                for cell in block:

                    if cell in house:
                        continue

                    if not cell.solved:
                        cell.remove_p_from_cell(number)

    return ("Pointing and Claiming", [])


# aggregate all solve methods into a list
solve_methods = [basic_elimination, naked_pair, x_wings, hidden_single, pointing_and_claiming]


# Reasonning process
def reasonning(game):

    while True:

        # count all p before this round
        p_count_before_round = game.possibility_count

        for m in solve_methods:

            # count all p before this method
            p_count_before_method = game.possibility_count

            # reasonning with method
            method, highlighted_cells = m(game)
        
            # Validate all cells
            game.validate_all_cells()

            # count all p after this round techniques
            p_count_after_method = game.possibility_count

            # If the method makes progress then show progress and restart from basic elimination
            # else try next method
            if not p_count_after_method == p_count_before_method:

                game.step += 1

                # show the result
                title = "Step " + str(game.step) + " " + str(method) + " result"
                game.show_progress_in_graphic(title, highlighted_cells)
                
                break

        # count all p after this round
        p_count_after_round = game.possibility_count

        # If no progress after applying all methods
        if p_count_before_round == p_count_after_round:

            # If is solved
            if game.is_solved():
                game.show_progress_in_graphic("Sudoku has been solved!")
                return

            # if still not
            else:
                game.show_progress_in_graphic("Final state and need more techniques!")
                return


# main function
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
    
    # reasonning solve
    reasonning(game)

if __name__ == "__main__":
    main()
