from pydantic import BaseModel
from typing import List, Tuple, Optional

class Obstacle(BaseModel):
    x: float
    y: float
    w: float
    h: float

class TrajectoryCreate(BaseModel):
    wall_width: float
    wall_height: float
    obstacles: List[Obstacle]
    name: Optional[str] = None
    step: Optional[float] = 0.5

class TrajectoryInDB(BaseModel):
    id: int
    created_at: str
    name: Optional[str]
    data: List[Tuple[float, float]]

class TrajectoryList(BaseModel):
    trajectories: List[TrajectoryInDB]
