import json
import pytest
from fastapi.testclient import TestClient

from backend.main import app, database
from backend import models

TEST_DATABASE_URL = "sqlite:///./test_trajectories.db"

def override_get_db():
    engine = database.create_engine(
        TEST_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = database.sessionmaker(bind=engine, autocommit=False, autoflush=False)
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[database.get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def run_around_tests():
    yield

def test_create_and_read_trajectory():
    payload = {
        "wall_width": 5.0,
        "wall_height": 5.0,
        "obstacles": [{"x": 2.0, "y": 2.0, "w": 0.25, "h": 0.25}],
        "step": 0.5,
    }
    response = client.post("/trajectories/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "data" in data
    trajectory_id = data["id"]

    get_resp = client.get(f"/trajectories/{trajectory_id}")
    assert get_resp.status_code == 200
    get_data = get_resp.json()
    assert get_data["id"] == trajectory_id
    assert isinstance(get_data["data"], list)

def test_list_trajectories():
    for _ in range(2):
        client.post("/trajectories/", json={
            "wall_width": 3.0,
            "wall_height": 3.0,
            "obstacles": [],
            "step": 1.0,
        })
    list_resp = client.get("/trajectories/")
    assert list_resp.status_code == 200
    list_data = list_resp.json()
    assert "trajectories" in list_data
    assert len(list_data["trajectories"]) >= 2
