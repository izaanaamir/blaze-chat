def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


def test_login(client):
    # First create a user
    client.post(
        "/users/",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "testpass",
        },
    )

    # Then try to login
    response = client.post(
        "/token", data={"username": "loginuser", "password": "testpass"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_create_conversation(client):
    # First create two users and get their tokens
    client.post(
        "/users/",
        json={
            "username": "user1",
            "email": "user1@example.com",
            "password": "pass1",
        },
    )
    client.post(
        "/users/",
        json={
            "username": "user2",
            "email": "user2@example.com",
            "password": "pass2",
        },
    )

    token_response = client.post(
        "/token", data={"username": "user1", "password": "pass1"}
    )
    token = token_response.json()["access_token"]

    response = client.post(
        "/messages/conversations/",
        headers={"Authorization": f"Bearer {token}"},
        json={"participant_ids": [1, 2]},
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data


def test_send_message(client):
    # Create users and conversation first
    client.post(
        "/users/",
        json={
            "username": "user1",
            "email": "user1@example.com",
            "password": "pass1",
        },
    )
    client.post(
        "/users/",
        json={
            "username": "user2",
            "email": "user2@example.com",
            "password": "pass2",
        },
    )

    token_response = client.post(
        "/token", data={"username": "user1", "password": "pass1"}
    )
    token = token_response.json()["access_token"]

    # Create conversation
    client.post(
        "/messages/conversations/",
        headers={"Authorization": f"Bearer {token}"},
        json={"participant_ids": [1, 2]},
    )

    # Send message
    response = client.post(
        "/messages/conversations/1/messages/",
        headers={"Authorization": f"Bearer {token}"},
        json={"content": "Test message"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Test message"
