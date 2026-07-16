from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from database import get_db
from database import Base
from main import app


TEST_DATABASE_URL = "postgresql://admin:password@localhost:5432/jobtracker_test"

test_engine = create_engine(TEST_DATABASE_URL, echo =True)
test_sessionLocal = sessionmaker(autocommit = False, bind = test_engine, autoflush = False)

Base.metadata.create_all(bind = test_engine)

def override_get_db():
    db = test_sessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)