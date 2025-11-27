from typing import Final

import pytest
from fastapi.testclient import TestClient

from bingo.api import app

API_ROUTE: Final[str] = "/api/v1/bingo/solve"

EXAMPLE_PAYLOAD = {
    "mode": "first",
    "numbers": [5, 8, 10, 3, 7, 2, 12, 9, 4, 6, 11, 1, 13, 14, 15, 16, 17],
    "boards": [
        [[5, 8, 10, 3, 7], [18, 19, 20, 21, 22], [1, 2, 4, 6, 9], [11, 12, 13, 14, 15], [16, 17, 23, 24, 25]],
        [[1, 16, 5, 22, 10], [2, 17, 6, 23, 11], [3, 18, 7, 24, 12], [4, 19, 8, 25, 13], [9, 14, 15, 20, 21]],
    ],
}


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_solve_endpoint_first_mode_returns_expected_score(client: TestClient) -> None:
    response = client.post(API_ROUTE, json=EXAMPLE_PAYLOAD)

    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert data["score"] == 2044


def test_solve_endpoint_last_mode_returns_expected_score(client: TestClient) -> None:
    payload = EXAMPLE_PAYLOAD
    payload["mode"] = "last"

    response = client.post(API_ROUTE, json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert data["score"] == 247


def test_solve_endpoint_invalid_board_shape(client: TestClient) -> None:
    bad_payload = {
        "numbers": [1, 2, 3, 4, 5],
        "boards": [
            [
                [1, 2, 3, 4, 5],
                [6, 7, 8, 9, 10],
                [11, 12, 13, 14, 15],
                [16, 17, 18, 19, 20],
            ]
        ],
    }

    response = client.post(API_ROUTE, json=bad_payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data and data["detail"] == "Board must be 5x5 square"
