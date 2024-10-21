from pydantic import BaseModel
from datetime import datetime
from typing import List


class GameCreate(BaseModel):
    player: str


class GameResponse(BaseModel):
    id: int
    player: str

    class Config:
        orm_mode = True


class GameFramesUpdate(BaseModel):
    frames: List[List[int]]  # List of lists of integers

    class Config:
        orm_mode = True
