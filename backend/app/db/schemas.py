from pydantic import BaseModel
from datetime import datetime
from typing import List


class GameCreate(BaseModel):
    """
    Schema for creating a new game.

    Attributes:
        player (str): The name of the player starting the game.
    """

    player: str


class GameResponse(BaseModel):
    """
    Schema for the response when a game is created.

    Attributes:
        id (int): The ID of the newly created game.
        player (str): The name of the player associated with the game.
    """

    id: int
    player: str

    class Config:
        orm_mode = True


class GameFramesUpdate(BaseModel):
    """
    Schema for updating the frames in a game.

    Attributes:
        frames (List[List[int]]): A list of lists of integers representing the rolls for each frame.
    """

    frames: List[List[int]]

    class Config:
        orm_mode = True
