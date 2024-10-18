from pydantic import BaseModel
from typing import List


class Game(BaseModel):
    id: int
    rolls: List[int] = []
    current_frame: int = 1
    completed: bool = False


class Roll(BaseModel):
    pins: int


def calculate_score(rolls: List[int]) -> int:
    score = 0
    roll_index = 0
    for frame in range(10):
        if rolls[roll_index] == 10:  # Strike all
            score += 10 + rolls[roll_index + 1] + rolls[roll_index + 2]
            roll_index += 1
        elif sum(rolls[roll_index : roll_index + 2]) == 10:  # Spare
            score += 10 + rolls[roll_index + 2]
            roll_index += 2
        else:
            score += sum(rolls[roll_index : roll_index + 2])
            roll_index += 2
    return score
