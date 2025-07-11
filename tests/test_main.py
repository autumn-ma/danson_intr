import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.database import Base, get_db
from src import crud, schemas
import os

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def test_file():
    file_path = "test_file.txt"
    with open(file_path, "w") as f:
        f.write("This is a test file.")
    yield file_path
    os.remove(file_path)

def test_upload_content(test_file, db_session):
    with open(test_file, "rb") as f:
        response = client.post("/upload-content/", files={"file": ("test_file.txt", f, "text/plain")})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "test_file.txt"
    assert data["content"] == "This is a test file."

def test_get_topics(db_session):
    content1 = schemas.ContentCreate(topic="Math", title="Algebra", grade="10", content="..." )
    content2 = schemas.ContentCreate(topic="Science", title="Physics", grade="11", content="...")
    crud.create_content(db_session, content1)
    crud.create_content(db_session, content2)

    response = client.get("/topics/")
    assert response.status_code == 200
    assert response.json() == {"topics": ["Math", "Science"]}

    response = client.get("/topics/?grade=10")
    assert response.status_code == 200
    assert response.json() == {"topics": ["Math"]}

def test_get_metrics(db_session):
    content1 = schemas.ContentCreate(topic="Math", title="Algebra", grade="10", content="...")
    content2 = schemas.ContentCreate(topic="Science", title="Physics", grade="11", content="...")
    crud.create_content(db_session, content1)
    crud.create_content(db_session, content2)

    response = client.get("/metrics/")
    assert response.status_code == 200
    assert response.json() == {"topics_count": 2, "files_uploaded": 2}

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to EduRAG!"}
