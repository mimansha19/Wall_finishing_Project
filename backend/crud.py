import json
from sqlalchemy.orm import Session
from . import models, schemas

def create_trajectory(
    db: Session,
    trajectory_in: schemas.TrajectoryCreate,
    trajectory_points: list,
) -> models.Trajectory:
    db_item = models.Trajectory(
        name=trajectory_in.name,
        data=json.dumps(trajectory_points),
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_trajectory(db: Session, trajectory_id: int) -> models.Trajectory:
    return db.query(models.Trajectory).filter(models.Trajectory.id == trajectory_id).first()


def list_trajectories(db: Session, skip: int = 0, limit: int = 100) -> list:
    return db.query(models.Trajectory).offset(skip).limit(limit).all()
