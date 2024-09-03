import pytest
from uuid import UUID


@pytest.fixture
def video_payload():
    return {
        "title": "Test Video",
        "description": "This is a test video",
        "video_url": "https://example.com/test-video.mp4",
        "image_url": "https://example.com/test-thumbnail.jpg",
        "tags": "test,video"
    }


@pytest.fixture
def video_payload_updated():
    return {
        "title": "Updated Test Video",
        "description": "This is an updated test video",
        "video_url": "https://example.com/updated-test-video.mp4",
        "image_url": "https://example.com/updated-test-thumbnail.jpg",
        "tags": "updated,test,video"
    }


def test_create_video(auth_client, video_payload):
    response = auth_client.post("/api/videos/", json=video_payload)
    assert response.status_code == 201
    response_json = response.json()
    assert response_json["Status"] == "Success"
    assert UUID(response_json["Video"]["id"])
    assert response_json["Video"]["title"] == video_payload["title"]
    assert response_json["Video"]["shared_by"]


def test_get_video(auth_client, video_payload):
    # Create a video
    create_response = auth_client.post("/api/videos/", json=video_payload)
    video_id = create_response.json()["Video"]["id"]

    # Get the created video
    response = auth_client.get(f"/api/videos/{video_id}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["Status"] == "Success"
    assert response_json["Video"]["id"] == video_id
    assert response_json["Video"]["title"] == video_payload["title"]


def test_list_videos(auth_client, video_payload):
    # Create a video
    auth_client.post("/api/videos/", json=video_payload)

    # List videos
    response = auth_client.get("/api/videos/")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["Status"] == "Success"
    assert len(response_json["Videos"]) > 0


def test_update_video(auth_client, video_payload, video_payload_updated):
    # Create a video
    create_response = auth_client.post("/api/videos/", json=video_payload)
    video_id = create_response.json()["Video"]["id"]

    # Update the video
    response = auth_client.patch(f"/api/videos/{video_id}", json=video_payload_updated)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["Status"] == "Success"
    assert response_json["Video"]["id"] == video_id
    assert response_json["Video"]["title"] == video_payload_updated["title"]


def test_delete_video(auth_client, video_payload):
    # Create a video
    create_response = auth_client.post("/api/videos/", json=video_payload)
    video_id = create_response.json()["Video"]["id"]

    # Delete the video
    response = auth_client.delete(f"/api/videos/{video_id}")
    assert response.status_code == 204

    # Try to get the deleted video
    get_response = auth_client.get(f"/api/videos/{video_id}")
    assert get_response.status_code == 404


def test_create_video_unauthenticated(test_client, video_payload):
    response = test_client.post("/api/videos/", json=video_payload)
    assert response.status_code == 401


def test_update_video_not_owner(auth_client, test_client, video_payload, video_payload_updated, user_payload):
    # Create a video with the first user
    create_response = auth_client.post("/api/videos/", json=video_payload)
    video_id = create_response.json()["Video"]["id"]

    # Create a second user and get their token
    test_client.post("/api/users/", json={
        "email": "second.user@example.com",
        "password": "password123"
    })
    login_response = test_client.post("/api/users/login", json={
        "email": "second.user@example.com",
        "password": "password123"
    })
    second_user_token = login_response.json()["access_token"]

    # Try to update the video with the second user
    headers = {"Authorization": f"Bearer {second_user_token}"}
    response = test_client.patch(f"/api/videos/{video_id}", json=video_payload_updated, headers=headers)
    assert response.status_code == 403


def test_delete_video_not_owner(auth_client, test_client, video_payload, user_payload):
    # Create a video with the first user
    create_response = auth_client.post("/api/videos/", json=video_payload)
    video_id = create_response.json()["Video"]["id"]

    # Create a second user and get their token
    test_client.post("/api/users/", json={
        "email": "second.user@example.com",
        "password": "password123"
    })
    login_response = test_client.post("/api/users/login", json={
        "email": "second.user@example.com",
        "password": "password123"
    })
    second_user_token = login_response.json()["access_token"]

    # Try to delete the video with the second user
    headers = {"Authorization": f"Bearer {second_user_token}"}
    response = test_client.delete(f"/api/videos/{video_id}", headers=headers)
    assert response.status_code == 403
