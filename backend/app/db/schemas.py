from pydantic import BaseModel, conint


# This will ensure `pins_knocked` is always between 0 and 10
class RollRequest(BaseModel):
    pins_knocked: conint(ge=0, le=10)
