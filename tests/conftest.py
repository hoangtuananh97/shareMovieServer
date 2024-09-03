import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, get_db
import io

from app.auth import create_access_token

# SQLite database URL for testing
SQLITE_DATABASE_URL = "sqlite:///./test_db.db"

# Create a SQLAlchemy engine
engine = create_engine(
    SQLITE_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create a sessionmaker to manage sessions
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables in the database
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a new database session with a rollback at the end of the test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def test_client(db_session):
    """Create a test client that uses the override_get_db fixture to return a session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


# Fixture to generate a random user id
@pytest.fixture()
def user_id() -> uuid.UUID:
    """Generate a random user id."""
    return str(uuid.uuid4())


@pytest.fixture()
def user_payload():
    """Generate a user payload."""
    return {
        "email": "john.doe@example.com",
        "password": "securepassword123"
    }


@pytest.fixture()
def user_payload_updated():
    """Generate an updated user payload."""
    return {
        "email": "jane.doe@example.com",
        "password": "newsecurepassword456"
    }


@pytest.fixture
def websocket_client():
    return TestClient(app)


@pytest.fixture()
def auth_token(test_client, user_payload):
    # Create a user
    response = test_client.post("/api/users/", json=user_payload)
    assert response.status_code == 201

    # Generate token
    access_token = create_access_token(data={"sub": user_payload["email"]})
    return access_token


@pytest.fixture()
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture()
def auth_client(test_client, auth_headers):
    test_client.headers.update(auth_headers)
    return test_client


@pytest.fixture()
def video_payload():
    return {
        "title": "Test Video",
        "description": "This is a test video",
        "video_url": "https://example.com/test-video.mp4",
        "image_url": "https://example.com/test-thumbnail.jpg",
        "tags": "test,video"
    }


@pytest.fixture()
def video_payload_updated():
    return {
        "title": "Updated Test Video",
        "description": "This is an updated test video",
        "video_url": "https://example.com/updated-test-video.mp4",
        "image_url": "https://example.com/updated-test-thumbnail.jpg",
        "tags": "updated,test,video"
    }


@pytest.fixture
def sample_image():
    return io.BytesIO(b"fake image content")


@pytest.fixture
def sample_video():
    return io.BytesIO(b"fake video content")
