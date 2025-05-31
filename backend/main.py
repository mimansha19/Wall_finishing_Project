import logging
import time
import json
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import database, schemas, crud, coverage_planner, models


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


database.init_db()

app = FastAPI(
    title="Wall Finishing Robot Control System API",
    description="Backend APIs for generating and storing wall finishing robot trajectories",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def log_requests_middleware(request: Request, call_next):
    start_time = time.time()
    response = None
    try:
        response = call_next(request)
        return response
    finally:
        process_time = (time.time() - start_time) * 1000
        logger.info(
            f"{request.method} {request.url.path} completed_in={process_time:.2f}ms"
        )

app.middleware("http")(log_requests_middleware)


@app.post("/trajectories/", response_model=schemas.TrajectoryInDB)
async def create_trajectory(
    trajectory_in: schemas.TrajectoryCreate, db: Session = Depends(get_db)
):
    
    obstacles = [ (obs.x, obs.y, obs.w, obs.h) for obs in trajectory_in.obstacles ]
    points = coverage_planner.generate_coverage_trajectory(
        wall_width=trajectory_in.wall_width,
        wall_height=trajectory_in.wall_height,
        obstacle_list=obstacles,
        step=trajectory_in.step or 0.5,
    )
    
    db_item = crud.create_trajectory(db=db, trajectory_in=trajectory_in, trajectory_points=points)
    
    return schemas.TrajectoryInDB(
        id=db_item.id,
        created_at=db_item.created_at.isoformat(),
        name=db_item.name,
        data=points,
    )


@app.get("/trajectories/{trajectory_id}", response_model=schemas.TrajectoryInDB)
async def read_trajectory(trajectory_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_trajectory(db, trajectory_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Trajectory not found")
    return schemas.TrajectoryInDB(
        id=db_item.id,
        created_at=db_item.created_at.isoformat(),
        name=db_item.name,
        data=json.loads(db_item.data),
    )


@app.get("/trajectories/", response_model=schemas.TrajectoryList)
async def list_all_trajectories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.list_trajectories(db, skip=skip, limit=limit)
    trajectories = []
    for item in items:
        trajectories.append(
            schemas.TrajectoryInDB(
                id=item.id,
                created_at=item.created_at.isoformat(),
                name=item.name,
                data=json.loads(item.data),
            )
        )
    return schemas.TrajectoryList(trajectories=trajectories)
