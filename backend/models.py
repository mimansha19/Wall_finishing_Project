from sqlalchemy import Column, Integer, DateTime, Text, func
from .database import Base

class Trajectory(Base):
    __tablename__ = "trajectories"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    name = Column(Text, nullable=True)
    data = Column(Text, nullable=False)  