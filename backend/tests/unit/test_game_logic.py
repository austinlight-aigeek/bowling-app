import pytest
from app.models.game import calculate_score


def test_calculate_score():
    # Example of a perfect game
    rolls = [10] * 12
    assert calculate_score(rolls) == 300

    # Example with spares
    rolls = [5, 5, 3] + [0] * 17
    assert calculate_score(rolls) == 16

    # Example normal game
    rolls = [1, 4, 4, 5, 6, 4, 5, 5, 10, 0, 1, 7, 3, 6, 4, 10, 2, 8, 6]
    assert calculate_score(rolls) == 133
