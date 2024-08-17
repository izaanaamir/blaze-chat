import requests
import threading
import time
from flask import Flask, request

app = Flask(__name__)

BASE_URL = "http://localhost:8000"
TOKEN = ""
CURRENT_USER = None
CONVERSATION_ID = None


@app.route("/webhook", methods=["POST"])
def webhook():
    event = request.json["event"]
    data = request.json["data"]
    if event == "new_message" and data["sender_id"] != CURRENT_USER["id"]:
        print(f"\n[New message] {data['sender_id']}: {data['content']}")
    elif event == "message_read":
        print(
            f"\n[Read receipt] Message {data['id']} was read at {data['read_at']}"  # noqa
        )
    return "", 204


def start_flask():
    app.run(port=5000)


def get_token(username, password):
    response = requests.post(
        f"{BASE_URL}/token", data={"username": username, "password": password}
    )
    return response.json()["access_token"]


def create_user(username, email, password):
    data = {"username": username, "email": email, "password": password}
    response = requests.post(f"{BASE_URL}/users/", json=data)
    return response.json()


def get_current_user():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    return response.json()


def create_conversation(participant_ids):
    headers = {"Authorization": f"Bearer {TOKEN}"}
    data = {"participant_ids": participant_ids}
    response = requests.post(
        f"{BASE_URL}/messages/conversations/", headers=headers, json=data
    )
    return response.json()


def send_message(conversation_id, content):
    headers = {"Authorization": f"Bearer {TOKEN}"}
    data = {"content": content, "message_type": "text"}
    response = requests.post(
        f"{BASE_URL}/messages/conversations/{conversation_id}/messages/",
        headers=headers,
        data=data,
    )
    return response.json()


def get_messages(conversation_id):
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(
        f"{BASE_URL}/messages/conversations/{conversation_id}/messages/",
        headers=headers,
    )
    return response.json()


def mark_message_read(message_id):
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.post(
        f"{BASE_URL}/messages/{message_id}/read", headers=headers
    )
    return response.json()


def login_or_create_user():
    global TOKEN, CURRENT_USER
    choice = input(
        "Do you want to (1) Login or (2) Create a new user? Enter 1 or 2: "
    )

    if choice == "1":
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        TOKEN = get_token(username, password)
    elif choice == "2":
        username = input("Enter a username: ")
        email = input("Enter your email: ")
        password = input("Enter a password: ")
        create_user(username, email, password)
        print("User created successfully. Please login.")
        TOKEN = get_token(username, password)
    else:
        print("Invalid choice. Exiting.")
        exit()

    CURRENT_USER = get_current_user()
    print(f"Logged in as {CURRENT_USER['username']}")


def start_or_join_conversation():
    global CONVERSATION_ID
    choice = input(
        "Do you want to (1) Start a new conversation or (2) Join an existing one? Enter 1 or 2: "  # noqa
    )

    if choice == "1":
        participant_ids = input(
            "Enter the IDs of participants (comma-separated, including your own ID): "  # noqa
        )
        participant_ids = [
            int(id.strip()) for id in participant_ids.split(",")
        ]
        conversation = create_conversation(participant_ids)
        CONVERSATION_ID = conversation["id"]
        print(f"Created conversation with ID: {CONVERSATION_ID}")
    elif choice == "2":
        CONVERSATION_ID = int(input("Enter the conversation ID: "))
    else:
        print("Invalid choice. Exiting.")
        exit()


def chat_interface():
    print(
        "\nChat interface started. Type your message and press Enter to send."
    )
    print("Type 'quit' to exit the chat.")

    # Start a thread to periodically fetch and display new messages
    def fetch_messages():
        last_message_id = 0
        while True:
            messages = get_messages(CONVERSATION_ID)
            for message in messages:
                if message["id"] > last_message_id:
                    if message["sender_id"] != CURRENT_USER["id"]:
                        print(
                            f"\n[New message] {message['sender_id']}: {message['content']}"  # noqa
                        )
                        mark_message_read(message["id"])
                    last_message_id = message["id"]
            time.sleep(2)  # Check for new messages every 2 seconds

    fetch_thread = threading.Thread(target=fetch_messages)
    fetch_thread.daemon = True
    fetch_thread.start()

    while True:
        message = input("")
        if message.lower() == "quit":
            break
        print(f"[Sent] You: {message}")


def main():
    login_or_create_user()
    start_or_join_conversation()
    chat_interface()


if __name__ == "__main__":
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()
    main()
