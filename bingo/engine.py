from collections import defaultdict

from bingo.settings import settings

BoardGrid = list[list[int]]


class BoardsManager:
    """
    Owns all boards + global number index and runs the game
    """

    def __init__(self, board_grids: list[BoardGrid]) -> None:
        self.boards: list[BingoBoard] = []
        self.global_index: defaultdict[int, list[int]] = defaultdict(list)

        for board_idx, grid in enumerate(board_grids):
            self.boards.append(board := BingoBoard(grid=grid))

            for number in board.number_index:
                self.global_index[number].append(board_idx)

    def play_until_first_win(self, numbers: list[int]) -> int:
        """
        Simulate drawing numbers until the first board wins

        Returns the score:
            (sum of unmarked numbers on winning board) * (last drawn number)
        """
        for number in numbers:
            for board_idx in self.global_index[number]:
                board = self.boards[board_idx]
                if board.mark(number):
                    return board.unmarked_sum() * number

        raise ValueError("No winning board found.")


class BingoBoard:
    """
    Single BOARD_SIZExBOARD_SIZE bingo board
    """

    def __init__(self, grid: BoardGrid) -> None:
        size = len(grid)
        if size != settings.BOARD_SIZE or any(len(row) != size for row in grid):
            raise ValueError(f"Board must be {settings.BOARD_SIZE}x{settings.BOARD_SIZE} square")

        self.grid = grid
        self.size = size
        self.has_won = False

        self.marked = [[False] * size for _ in range(size)]
        self.number_index = defaultdict(list)
        self.row_counts = [0] * size
        self.col_counts = [0] * size

        for row_idx, row in enumerate(self.grid):
            for col_idx, number in enumerate(row):
                self.number_index[number].append((row_idx, col_idx))

    def mark(self, number: int) -> bool:
        """
        Mark `number` on this board

        Returns True if this call makes the board win for the first time
        """
        if self.has_won:
            return False

        positions = self.number_index.get(number)
        if not positions:
            return False

        for row, col in positions:
            if self.marked[row][col]:
                continue

            self.marked[row][col] = True
            self.row_counts[row] += 1
            self.col_counts[col] += 1

            if self.row_counts[row] == self.size or self.col_counts[col] == self.size:
                self.has_won = True
                return True

        return False

    def unmarked_sum(self) -> int:
        """
        Sum of all numbers that are not yet marked on this board
        """
        board_range = range(self.size)
        return sum(self.grid[row][col] for row in board_range for col in board_range if not self.marked[row][col])


def find_first_winner_score(numbers: list[int], board_grids: list[BoardGrid]) -> int:
    manager = BoardsManager(board_grids)
    return manager.play_until_first_win(numbers)
