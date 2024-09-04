import time
from uuid import UUID


def test_root(test_client):
    response = test_client.get("/api/healthchecker")
    assert response.status_code == 200
    assert response.json() == {"message": "The API is LIVE!!"}


def test_create_user(test_client, user_payload):
    response = test_client.post("/api/users/", json=user_payload)
    assert response.status_code == 201
    response_json = response.json()
    assert response_json["Status"] == "Success"
    assert UUID(response_json["User"]["id"])
    assert response_json["User"]["email"] == user_payload["email"]
    assert "password" not in response_json["User"]


def test_get_user(auth_client, user_payload):
    # Get the created user
    response = auth_client.get("/api/users/")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "Success"
    assert len(response_json["users"]) > 0
    user = response_json["users"][0]
    assert user["email"] == user_payload["email"]
    assert "password" not in user


def test_update_user(auth_client, user_payload, user_payload_updated):
    # Get the user ID
    response = auth_client.get("/api/users/")
    user_id = response.json()["users"][0]["id"]

    # Update the created user
    time.sleep(1)  # Sleep for 1 second to ensure updatedAt is different
    response = auth_client.patch(f"/api/users/{user_id}", json=user_payload_updated)
    assert response.status_code == 202
    response_json = response.json()
    assert response_json["Status"] == "Success"
    assert response_json["User"]["id"] == user_id
    assert response_json["User"]["email"] == user_payload_updated["email"]
    assert "password" not in response_json["User"]


def test_delete_user(auth_client):
    # Get the user ID
    response = auth_client.get("/api/users/")
    user_id = response.json()["users"][0]["id"]

    # Delete the created user
    response = auth_client.delete(f"/api/users/{user_id}")
    assert response.status_code == 202
    response_json = response.json()
    assert response_json["Status"] == "Success"
    assert response_json["Message"] == "User deleted successfully"

    # Get the deleted user
    response = auth_client.get(f"/api/users/{user_id}")
    assert response.status_code == 401


def test_get_user_not_found(auth_client):
    non_existent_id = str(UUID(int=0))
    response = auth_client.get(f"/api/users/{non_existent_id}")
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == f"No User with this id: `{non_existent_id}` found"


def test_create_user_wrong_payload(test_client):
    response = test_client.post("/api/users/", json={})
    assert response.status_code == 422


def test_update_user_wrong_payload(auth_client, user_payload_updated):
    # Get the user ID
    response = auth_client.get("/api/users/")
    user_id = response.json()["users"][0]["id"]

    invalid_payload = {"email": "not_an_email"}
    response = auth_client.patch(f"/api/users/{user_id}", json=invalid_payload)
    assert response.status_code == 422
    response_json = response.json()
    assert "detail" in response_json


def test_update_user_doesnt_exist(auth_client, user_payload_updated):
    non_existent_id = str(UUID(int=0))
    response = auth_client.patch(f"/api/users/{non_existent_id}", json=user_payload_updated)
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == f"No User with this id: `{non_existent_id}` found"


def test_create_user_duplicate_email(test_client, user_payload):
    # Create a user
    response = test_client.post("/api/users/", json=user_payload)
    assert response.status_code == 201

    # Try to create another user with the same email
    response = test_client.post("/api/users/", json=user_payload)
    assert response.status_code == 409
    response_json = response.json()
    assert response_json["detail"] == "A user with this email already exists."


def test_unauthenticated_access(test_client):
    response = test_client.get("/api/users/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_user_login(test_client, user_payload):
    # Create a user
    test_client.post("/api/users/", json=user_payload)

    # Login
    login_data = {
        "email": user_payload["email"],
        "password": user_payload["password"]
    }
    response = test_client.post("/api/users/login", json=login_data)
    assert response.status_code == 200
    response_json = response.json()
    assert "access_token" in response_json
    assert "token_type" in response_json
    assert response_json["token_type"] == "bearer"


def test_invalid_login(test_client, user_payload):
    # Create a user
    test_client.post("/api/users/", json=user_payload)

    # Try to login with wrong password
    login_data = {
        "email": user_payload["email"],
        "password": "wrong_password"
    }
    response = test_client.post("/api/users/login", json=login_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


def test_update_user_password(auth_client, user_payload):
    # Get the user ID
    response = auth_client.get("/api/users/")
    user_id = response.json()["users"][0]["id"]

    # Update password
    new_password = "new_secure_password123"
    update_payload = {"password": new_password}
    response = auth_client.patch(f"/api/users/{user_id}", json=update_payload)
    assert response.status_code == 202
    response_json = response.json()
    assert response_json["Status"] == "Success"
    assert "password" not in response_json["User"]

    # try to login with the new password
    login_data = {
        "email": user_payload["email"],
        "password": new_password
    }
    login_response = auth_client.post("/api/users/login", json=login_data)
    assert login_response.status_code == 200


def test_create_user_invalid_email(test_client):
    invalid_user_payload = {
        "email": "not_an_email",
        "password": "securepassword123"
    }
    response = test_client.post("/api/users/", json=invalid_user_payload)
    assert response.status_code == 422
    response_json = response.json()
    assert "detail" in response_json
    assert any(error["loc"] == ["body", "email"] for error in response_json["detail"])


def test_create_user_empty_email(test_client):
    invalid_user_payload = {
        "email": "",
        "password": "securepassword123"
    }
    response = test_client.post("/api/users/", json=invalid_user_payload)
    assert response.status_code == 422
    response_json = response.json()
    assert "detail" in response_json
    assert any(error["loc"] == ["body", "email"] for error in response_json["detail"])


def test_create_user_empty_password(test_client):
    invalid_user_payload = {
        "email": "abc@gmail.com",
        "password": ""
    }
    response = test_client.post("/api/users/", json=invalid_user_payload)
    print(response.json())
    assert response.status_code == 422
    response_json = response.json()

    assert "detail" in response_json
    assert response_json["detail"] == [
        {
            'type': 'string_too_short',
            'loc': ['body', 'password'],
            'msg': 'String should have at least 8 characters',
            'input': '', 'ctx': {'min_length': 8}
        }
    ]


def test_create_user_invalid_payload(test_client):
    # Attempt to create a user with an invalid payload
    invalid_payload = {
        "email": "invalid-email",  # Invalid email format
        "password": "123"  # Password too short
    }
    response = test_client.post("/api/users/", json=invalid_payload)

    assert response.status_code == 422
    assert "detail" in response.json()


def test_delete_user_not_found(auth_client):
    non_existent_user_id = "non-existent-id"
    response = auth_client.delete(f"/api/users/{non_existent_user_id}")

    assert response.status_code == 500
