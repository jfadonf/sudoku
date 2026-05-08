from copy import deepcopy


class Cell:
    def __init__(self, possibilities=None):

        if possibilities is None:
            possibilities = {1,2,3,4,5,6,7,8,9}

        self.possibilities: set[int] = set(possibilities)

        if len(self.possibilities) == 0:
            raise ValueError("No possibilities here!")

    @property
    def solved(self) -> bool:
        return len(self.possibilities) == 1

    def value(self) -> int:
        return next(iter(self.possibilities))

    def __len__(self):
        return len(self.possibilities)

    def __repr__(self):
        return str(self.possibilities)


class Sudoku:
    def __init__(self, text: str):
        lines = text.strip().splitlines()
        self.grid: list[list[Cell]] = []
        for line in lines:
            row = []
            for ch in line:
                n = int(ch)
                if n == 0:
                    row.append(Cell())
                else:
                    row.append(Cell({n}))
            self.grid.append(row)

    def show(self):
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

game = Sudoku(puzzle)

game.show()
