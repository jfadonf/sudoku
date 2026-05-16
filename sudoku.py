# to copy nested list
from copy import deepcopy

# to draw the Sudoku in graphic
import matplotlib.pyplot as plt

# the class of single cell:
# __init__ with the possibilities
class Cell:

    row_number: int
    column_number: int
    block_number: int
    p: set[int]
    row: House
    column: House
    block: House
    row_peers: House
    column_peers: House
    block_peers: House

    #
    def __init__(self, r, c, possibilities=None):
        self.row_number = r
        self.column_number = c
        self.block_number = ((r - 1) // 3) * 3 + ((c - 1) // 3) + 1

        if possibilities is None:
            possibilities = {1,2,3,4,5,6,7,8,9}

        self.p = set(possibilities)


        self.row = None
        self.column = None
        self.block = None

    def remove(self, n):
        self.p.discard(n)
        if len(self.p) == 0:
            print(f"The cell r: {self.row}, c: {self.column}")
            raise ValueError(f"No possibilities here!")

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

    # method: remove number from all unsolved cells' p in a house
    def remove_p(self, number, cells_exempted):
        for cell in self:
            if cell.is_solved() or cell in cells_exempted:
                continue
            cell.remove(number)

    def __iter__(self):
        return iter(self.cells)

    def __len__(self):
        return len(self.cells)

    def __repr__(self):
        return f"{self.house_type} {self.index}"

    # method: find_p(p, count=0)
    # if count is absent, return all the cells with p
    # if count is passed, if there count cells, return the [cells], 
    # other wise return []
    def find_p(self, p, count=0):

        cells = []

        for cell in self:
            if not cell.is_solved():
                if p in cell.p:
                    cells.append(cell)

        if count == 0:
            return cells
        elif len(cells) == count:
            return cells
        else:
            return []

# the class of Sudoku grid
# __init__ with multiline str
# function to show_stage_in_str
# function to show_stage_in_graphic
# function to show_progress_in_graphic
class Sudoku:

    grid: list[list[Cell]]
    unsolved: House
    step: int = 0

    def __init__(self, text: str):

        self.grid = []
        self.unsolved = House("Unsolved", 0)

        # Instanciate RCB houses
        self.rows = [House("Row", i) for i in range(9)]
        self.columns = [House("Column", i) for i in range(9)]
        self.blocks = [House("Block", i) for i in range(9)]


        # Instanciate cells,
        lines = text.strip().splitlines()

        for r, line in enumerate(lines):
            row = []
            for c, ch in enumerate(line):
                n = int(ch)
                if n == 0:
                    cell = Cell(r, c)
                    self.unsolved.add(cell)
                else:
                    cell = Cell(r, c, {n})

                # assign RCB houses to the cell's attributes
                cell.row = self.rows[r]
                cell.column = self.columns[c]
                block_index = (r // 3) * 3 + (c // 3)
                cell.block = self.blocks[block_index]

                # add cell into RCB houses
                self.rows[r].add(cell)
                self.columns[c].add(cell)
                self.blocks[block_index].add(cell)

                row.append(cell)

            self.grid.append(row)

        # Initialize peers of all cells with its own peers of RCB
        for r in range(9):
            for c in range(9):
                cell = self.grid[r][c]

                block_index = (r // 3) * 3 + (c // 3)

                row_peers = House("Row Peers", str(r * 10 + c))
                column_peers = House("Colume Peers", str(r * 10 + c))
                block_peers = House("Block Peers", block_index)

                for peer in self.rows[r]:
                    row_peers.add(peer)
                row_peers.remove(cell)
                cell.row_peers = row_peers

                for peer in self.columns[c]:
                    column_peers.add(peer)
                column_peers.remove(cell)
                cell.column_peers = column_peers

                block_index = (r // 3) * 3 + (c // 3)
                for peer in self.blocks[block_index]:
                    block_peers.add(peer)
                block_peers.remove(cell)
                cell.block_peers = block_peers

    def show_progress_in_str(self):

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

    def show_progress_in_graphic(self, title, show_p=True):
        fig, ax = plt.subplots(figsize=(9, 9))
        fig.suptitle(title, fontsize=24)
        ax.set_title(
            f"Remaining unsolved cells: {len(self.unsolved)}\nTatol remaining possibilities: {self.p_count()-81}",
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
                elif show_p:
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

    # to know if technique make any progress, count all p
    def p_count(self):
        count_p = 0
        for r in range(9):
            for c in range(9):
                count_p += len(self.grid[r][c].p)
        return count_p


    def is_solved(self):
        return not self.unsolved

    def validate(self, cell):
        if cell.is_solved() and cell in self.unsolved:
            self.unsolved.remove(cell)
        if not cell.is_solved() and not cell in self.unsolved:
            self.unsolved.add(cell)



    # Solve method: Basic elimination
    # remove all the numbers occurs at the same row,
    # column and block, for all unsolved cells.
    # This can remove ps and solve cells
    def basic_elimination(self):
        # index of newly solved cells
        newly_solved = []
        p_removed = False

        # for each unsolved cells
        for index, question_cell in enumerate(self.unsolved):

            # remove the number of solved cells from possibilities
            for cell in question_cell.row_peers:
                if cell.is_solved():
                    p_len = len(question_cell.p)
                    question_cell.remove(cell.value())
                    if p_len != len(question_cell):
                        p_removed = True

            for cell in question_cell.column_peers:
                if cell.is_solved():
                    p_len = len(question_cell.p)
                    question_cell.remove(cell.value())
                    if p_len != len(question_cell):
                        p_removed = True

            for cell in question_cell.block_peers:
                if cell.is_solved():
                    p_len = len(question_cell.p)
                    question_cell.remove(cell.value())
                    if p_len != len(question_cell):
                        p_removed = True

            # if possibility has been removed then
            if p_removed:

                # if the question_cell has newly solved then
                # save the index of newly solved cells
                if question_cell.is_solved:
                    newly_solved.append(question_cell)

        # if any new solved cell
        if newly_solved:

            # remove solved cells from unsolved list
            for cell in newly_solved:
                self.validate(cell)

            # step += 1 and show sudoku state
            self.step += 1
            title = "Step " + str(self.step) + " Basic Elimination result"
            self.show_progress_in_graphic(title)

            # return True if made progress
            return True
        else:
            return False

    # Solve method: Hidden Singles
    # This searcheshe hidden singles in all House class.
    # This can solve cells
    def hidden_single(self):
        newly_solved = []


        # search in all RCB
        for house in self.rows + self.columns + self.blocks:

            # count candidate occurrences
            number_occurrences = {}

            for i in range(1, 10):
                number_occurrences[i] = []

            # iterate all cells but solved ones
            for cell in house:
                if cell.is_solved():
                    continue
                else:
                    for p in cell.p:
                        number_occurrences[p].append(cell)

            # hidden single check
            for number, cells in number_occurrences.items():
                if len(cells) == 1:
                    target = cells[0]
                    newly_solved.append((target, number))

        # if any newly solved, show sudoku state and step += 1
        if newly_solved:

            # solve the cells and remove them from unsolved
            for cell, number in newly_solved:
                cell.p = {number}
                self.validate(cell)

            # show the result
            self.step += 1
            title = "Step " + str(self.step) + " Hidden Single result"
            self.show_progress_in_graphic(title)

            return True
        else:
            return False

    # Solve method: Naked Pairs
    # This searchess naked pairs in all Houses.
    # This can remove ps.
    def naked_pair(self):

        p_count_before = self.p_count()

        # searching naked pairs in all houses
        # iterate all houes
        # find cells with the same possibility set to get a pair
        # if the possibility count equals the cell count in the pair
        # remove the possibilities in the set from all the other cells in the house

        # search all houses
        for house in self.rows + self.columns + self.blocks:

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

                if cell.is_solved():
                    continue

                key = frozenset(cell.p)

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

                        for n in p_set:

                            if n in other.p:
                                other.p.discard(n)

                                self.validate(other)

        # progress check: if any p removed, show sudoku state and step += 1
        if p_count_before != self.p_count():

            # show the result
            self.step += 1
            title = "Step " + str(self.step) + " Naked Pair result"
            self.show_progress_in_graphic(title)

            return True
        else:
            return False

    # Solve method: X_Wings
    def x_wings(self):

        p_count_before = self.p_count()

        # 1. find 2 n in row or column houses
        for n in range(1, 10):

            # row section
            for row_number1 in range(0, 9):

                c12 = self.rows[row_number1].find_p(n, 2)

                if len(c12) == 2:

                    c1, c2 = c12[0], c12[1]

                    # 2. find 2 n in row2 at same places
                    for row_number2 in range(row_number1 + 1, 9):

                        c34 = self.rows[row_number2].find_p(n, 2)

                        if len(c34) == 2:

                            c3, c4 = c34[0], c34[1]

                            if c1.column_number == c3.column_number and c2.column_number == c4.column_number:

                                # 3. remove n from the places' perpendicular houses' cells' p
                                self.columns[c1.column_number].remove_p(n, c12 + c34)
                                self.columns[c2.column_number].remove_p(n, c12 + c34)

            # column section
            for column_number1 in range(0, 9):

                c12 = self.columns[column_number1].find_p(n, 2)

                if len(c12) == 2:

                    c1, c2 = c12[0], c12[1]

                    # 2. find 2 n in 2 at same places
                    for column_number2 in range(column_number1 + 1, 9):

                        c34 = self.columns[column_number2].find_p(n, 2)

                        if len(c34) == 2:

                            c3, c4 = c34[0], c34[1]

                            if c1.row_number == c3.row_number and c2.row_number == c4.row_number:

                                # 3. remove n from the places' perpendicular houses' cells' p
                                self.rows[c1.row_number].remove_p(n, c12 + c34)
                                self.rows[c2.row_number].remove_p(n, c12 + c34)

        # progress check: if any p removed, show sudoku state and step += 1
        if p_count_before != self.p_count():

            # show the result
            self.step += 1
            title = "Step " + str(self.step) + " X Wings result"
            self.show_progress_in_graphic(title)

            return True
        else:
            return False

    # Solve method: Pointing
    # if all p of certain number locate one row or column in a block
    # then remove the number from the other cells of the line
    def pointing(self):

        p_count_before = self.p_count()

        # iteration numbers in iteration of blocks
        for block in self.blocks:

            for number in range(1, 10):

                cells = [c for c in block if number in c.p]

                if not cells:
                    continue

                # check same row
                rows = {c.row for c in cells}

                if len(rows) == 1:

                    row = next(iter(rows))

                    for cell in row:

                        if cell in block:
                            continue

                        if not cell.is_solved():
                            cell.remove(number)

                # check same column
                columns = {c.column for c in cells}

                if len(columns) == 1:

                    column = next(iter(columns))

                    for cell in column:

                        if cell in block:
                            continue

                        if not cell.is_solved():
                            cell.remove(number)

        # progress check: if any p removed, show sudoku state and step += 1
        if p_count_before != self.p_count():

            # show the result
            self.step += 1
            title = "Step " + str(self.step) + " Pointing result"
            self.show_progress_in_graphic(title)

            return True
        else:
            return False
                



def main():
    # example of Sudoku str
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

### TEST EREA ###
#    print(game.blocks[0].cells)
#     print(game.grid[3][4].column_number)
#     print(game.grid[3][4].block_number)
#     print(game.grid[3][4].value())
#
#     print(game.grid[3][4].row)
#     print(game.grid[3][4].column)
#     print(game.grid[3][4].block)
#
#     print(game.grid[3][4].row_peers.cells)
#     print(game.grid[3][4].column_peers.cells)
#     print(game.grid[3][4].block_peers.cells)
### TEST EREA ###

    # PROCESS OF SOLVING
    while True:
        # count all p before this round techniques
        p_count_before = game.p_count()

        # Technique: Basic eliminations
        if game.basic_elimination():
            continue

        # Technique: X Wings
        if game.x_wings():
            continue

        # Technique: pointing
        if game.pointing():
            continue

        # Technique: hidden single
        if game.hidden_single():
            continue

        # Technique: naked pair
        if game.naked_pair():
            continue

        # count all p after this round techniques
        p_count_after = game.p_count()

        # If it makes no progress after all methods
        if p_count_after == p_count_before:

            # If is solved
            if game.is_solved():
                game.show_progress_in_graphic("Sudoku has been solved!")
                return
            else:
                game.show_progress_in_graphic("Final state and need more techniques!")
                return

if __name__ == "__main__":
    main()
