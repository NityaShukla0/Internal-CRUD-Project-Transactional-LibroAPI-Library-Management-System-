import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db

# ------------------------------------------------------
# 1. POSTGRES TEST DATABASE URL
# ------------------------------------------------------
TEST_DATABASE_URL = (
    "postgresql+psycopg2://nityashukla:password123@localhost:5432/libro_test_db"
)

# ------------------------------------------------------
# 2. TEST ENGINE + SESSION
# ------------------------------------------------------
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# ------------------------------------------------------
# 3. CREATE CLEAN TABLES BEFORE TEST SESSION
# ------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# ------------------------------------------------------
# 4. OVERRIDE get_db() FOR FASTAPI
# ------------------------------------------------------
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

app.dependency_overrides[get_db] = override_get_db

# ------------------------------------------------------
# 5. db_session FIXTURE (needed for tests/test_crud.py)
# ------------------------------------------------------
@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
        db.commit()
    finally:
        db.rollback()
        db.close()
# ------------------------------------------------------
# 6. TEST CLIENT FIXTURE
# ------------------------------------------------------
@pytest.fixture()
def client():
    return TestClient(app)