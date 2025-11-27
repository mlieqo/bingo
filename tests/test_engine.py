import pytest

from bingo.engine import (
    BingoBoard,
    BoardsManager,
    find_first_winner_score,
    find_last_winner_score,
)
from tests.test_api import EXAMPLE_PAYLOAD

EXAMPLE_NUMBERS = EXAMPLE_PAYLOAD["numbers"]
EXAMPLE_BOARDS = EXAMPLE_PAYLOAD["boards"]


def test_find_first_winner_score_matches() -> None:
    score = find_first_winner_score(EXAMPLE_NUMBERS, EXAMPLE_BOARDS)  # type: ignore[arg-type]
    assert score == 2044


def test_find_last_winner_score_matches() -> None:
    score = find_last_winner_score(EXAMPLE_NUMBERS, EXAMPLE_BOARDS)  # type: ignore[arg-type]
    assert score == 247


@pytest.mark.parametrize(
    "number, expected_indices",
    [
        (14, {0, 1}),
        (25, {0, 1}),
        (26, set()),
        (99, set()),
    ],
)
def test_boards_manager_global_index(number: int, expected_indices: set[int]) -> None:
    manager = BoardsManager(EXAMPLE_BOARDS)  # type: ignore[arg-type]

    indices_from_index = set(manager.global_index[number])
    assert indices_from_index == expected_indices

    for idx in indices_from_index:
        grid = manager.boards[idx].grid
        assert any(number in row for row in grid)


def test_bingo_board_marks_and_unmarked_sum() -> None:
    grid = [
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25],
    ]

    board = BingoBoard(grid)

    assert board.mark(1) is False
    assert board.mark(2) is False
    assert board.mark(3) is False
    assert board.mark(4) is False

    assert board.has_won is False

    assert board.mark(5) is True
    assert board.has_won is True

    # Why mypy?
    total = sum(range(1, 25 + 1))  # type: ignore[unreachable]
    expected_unmarked = total - sum(range(1, 6))

    assert board.unmarked_sum() == expected_unmarked


def test_invalid_board_shape_raises() -> None:
    bad_board = [
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
    ]
    with pytest.raises(ValueError):
        BingoBoard(bad_board)


def test_two_boards_win_on_same_number_first_index_wins_for_first_mode() -> None:
    """If two boards win on the same draw, first-winner logic should pick the lower index."""
    numbers = [1, 2, 3, 4, 5]

    board0 = [
        [1, 2, 3, 4, 5],
        [10, 11, 12, 13, 14],
        [15, 16, 17, 18, 19],
        [20, 21, 22, 23, 24],
        [25, 26, 27, 28, 29],
    ]
    board1 = [
        [30, 31, 32, 33, 34],
        [1, 2, 3, 4, 5],
        [35, 36, 37, 38, 39],
        [40, 41, 42, 43, 44],
        [45, 46, 47, 48, 49],
    ]

    boards = [board0, board1]

    score = find_first_winner_score(numbers, boards)

    total0 = sum(sum(row) for row in board0)
    expected_unmarked0 = total0 - sum([1, 2, 3, 4, 5])
    expected_score0 = expected_unmarked0 * 5

    assert score == expected_score0
