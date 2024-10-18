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
        if roll_index >= len(rolls):
            break  # No more rolls to calculate score

        if rolls[roll_index] == 10:  # Strike
            if roll_index + 2 < len(
                rolls
            ):  # Ensure there are enough rolls for the strike bonus
                score += 10 + rolls[roll_index + 1] + rolls[roll_index + 2]
            roll_index += 1
        elif (
            roll_index + 1 < len(rolls)
            and sum(rolls[roll_index : roll_index + 2]) == 10
        ):  # Spare
            if roll_index + 2 < len(
                rolls
            ):  # Ensure there is enough roll for the spare bonus
                score += 10 + rolls[roll_index + 2]
            roll_index += 2
        else:
            if roll_index + 1 < len(
                rolls
            ):  # Ensure there are enough rolls for this frame
                score += sum(rolls[roll_index : roll_index + 2])
            roll_index += 2
    return score
