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
    def __init__(self, sudoku):
        self.grid: list[list[Cell]] = deepcopy(sudoku)

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



sudoku_data = [
    [Cell({5}), Cell({3}), Cell({1,2,4}), Cell({2,6}), Cell({7}), Cell({2,4,6,8}), Cell({1,4,8,9}), Cell({1,2,4,9}), Cell({2,4,8})],

    [Cell({6}), Cell({2,4,7}), Cell({2,4,7}), Cell({1}), Cell({9}), Cell({5}), Cell({3,4,7,8}), Cell({2,3,4}), Cell({2,4,7,8})],

    [Cell({1,2}), Cell({9}), Cell({8}), Cell({2,3}), Cell({3,4}), Cell({2,4}), Cell({1,3,4,5,7}), Cell({6}), Cell({2,4,7})],

    [Cell({8}), Cell({1,2,5}), Cell({1,2,5,9}), Cell({7}), Cell({6}), Cell({1,4}), Cell({4,5,7,9}), Cell({2,4,5,9}), Cell({3})],

    [Cell({4}), Cell({2,5}), Cell({2,5,6,9}), Cell({8}), Cell({5}), Cell({3}), Cell({7,9}), Cell({2,5,9}), Cell({1})],

    [Cell({7}), Cell({1,5}), Cell({1,3,5,9}), Cell({9}), Cell({2}), Cell({1,4}), Cell({4,5,8}), Cell({4,5}), Cell({6})],

    [Cell({1,3,9}), Cell({6}), Cell({1,3,4,5,7,9}), Cell({3,5}), Cell({3}), Cell({7}), Cell({2}), Cell({8}), Cell({4})],

    [Cell({2,3}), Cell({2,7,8}), Cell({2,3,7}), Cell({4}), Cell({1}), Cell({9}), Cell({6}), Cell({3,7}), Cell({5})],

    [Cell({1,2,3}), Cell({1,2,4,5}), Cell({1,2,3,4,5}), Cell({2,3,5,6}), Cell({8}), Cell({2,6}), Cell({1,3,4,7,9}), Cell({7}), Cell({9})],
]

game = Sudoku(sudoku_data)

game.show()
