# Wall Finishing Robot Control System

This repository contains a backend service built with FastAPI and SQLite for generating and storing wall coverage trajectories for an autonomous wall-finishing robot, as well as a simple frontend to visualize the generated coverage path.

## Backend Setup

1. Create a virtual environment and install dependencies:

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run the FastAPI application:

   ```bash
   uvicorn backend.main:app --reload
   ```

   The API will be available at `http://localhost:8000`.

3. Endpoints:
   - `POST /trajectories/` : Generate and store a coverage trajectory. Expects JSON body with `wall_width`, `wall_height`, `obstacles`, and optional `step`.
   - `GET /trajectories/{trajectory_id}` : Retrieve a stored trajectory by ID.
   - `GET /trajectories/` : List all stored trajectories.

## Frontend Setup

1. cd frontend
2. start index.html

## Testing

1. Install testing dependencies (from backend requirements). Ensure pytest is installed.

2. Run tests:

   ```bash
   pytest
   ```

## Sample Case

- Wall: 5m x 5m
- Obstacle: Window (0.25m x 0.25m) at (2m, 2m)

Example JSON for POST `/trajectories/`:

```json
{
  "wall_width": 5.0,
  "wall_height": 5.0,
  "obstacles": [{ "x": 2.0, "y": 2.0, "w": 0.25, "h": 0.25 }],
  "step": 0.5
}
```

This will generate a coverage path that avoids the obstacle and store it in the SQLite database `trajectories.db`.
