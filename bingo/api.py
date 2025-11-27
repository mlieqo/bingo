from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, model_validator

from bingo.engine import BoardGrid, find_first_winner_score, find_last_winner_score


class SolveRequest(BaseModel):
    mode: Literal["first", "last"] = Field(
        default="first",
        description='Which variant to solve: "first" for the first winning board, "last" for the last winning board.',
        examples=["first"],
    )
    numbers: list[int] = Field(
        description="Drawn numbers in order.",
        examples=[[5, 8, 10, 3, 7, 2, 12, 9, 4, 6, 11, 1, 13, 14, 15, 16, 17]],
    )
    boards: list[BoardGrid] = Field(
        description="List of boards as BOARD_SIZExBOARD_SIZE integer grids.",
        examples=[
            [
                [
                    [5, 8, 10, 3, 7],
                    [18, 19, 20, 21, 22],
                    [1, 2, 4, 6, 9],
                    [11, 12, 13, 14, 15],
                    [16, 17, 23, 24, 25],
                ],
                [
                    [1, 16, 5, 22, 10],
                    [2, 17, 6, 23, 11],
                    [3, 18, 7, 24, 12],
                    [4, 19, 8, 25, 13],
                    [9, 14, 15, 20, 21],
                ],
            ]
        ],
    )

    @model_validator(mode="after")
    def validate_boards(self) -> "SolveRequest":
        if not self.boards:
            raise ValueError("At least one board must be provided.")

        for idx, board in enumerate(self.boards):
            if len(board) == 0:
                raise ValueError(f"Board {idx} is empty.")
        return self


class SolveResponse(BaseModel):
    score: int


app = FastAPI(
    title="Bingo Solver API",
    description=(
        "API wrapper around Advent of Code - bingo game\n\nInput is JSON: drawn numbers + list of boards as 2D arrays."
    ),
)


@app.post("/api/v1/bingo/solve", response_model=SolveResponse)
def solve_bingo(request: SolveRequest) -> SolveResponse:
    numbers = request.numbers
    boards = request.boards

    try:
        if request.mode == "first":
            score = find_first_winner_score(numbers, boards)
        else:
            score = find_last_winner_score(numbers, boards)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e

    return SolveResponse(score=score)
