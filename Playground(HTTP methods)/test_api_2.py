from enum import Enum

from fastapi import FastAPI

app = FastAPI()


# note that by using Enumerations, you can pre-define some values
# and provide them for Users/Customers.
# like using Enum for drop-down-boxes or some optional components
# in UI that you need to choose some confined options.
class Direction(Enum):
    north = "North"
    south = "South"
    east = "East"
    west = "West"


@app.get("/directions/{direction_name}")
async def get_direction(direction_name: Direction):
    if direction_name == Direction.north:
        return {"direction_name": direction_name, "way": "UP"}

    if direction_name == Direction.south:
        return {"direction_name": direction_name, "way": "DOWN"}

    if direction_name == Direction.east:
        return {"direction_name": direction_name, "way": "RIGHT"}

    if direction_name == Direction.west:
        return {"direction_name": direction_name, "way": "LEFT"}
