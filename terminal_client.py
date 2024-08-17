import requests
import os
import time

BASE_URL = "http://localhost:8000"
TOKEN = ""
CURRENT_USER = None


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


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
    data = {"content": content}
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


def get_conversations():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(
        f"{BASE_URL}/messages/conversations/", headers=headers
    )
    return response.json()


def login_or_create_user():
    global TOKEN, CURRENT_USER
    clear_screen()
    print("Welcome to the Messaging App!")
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
    input("Press Enter to continue...")


def display_menu():
    clear_screen()
    print(f"Welcome, {CURRENT_USER['username']}!")
    print("\n1. View Conversations")
    print("2. Send a Message")
    print("3. Logout")
    print("4. Exit")
    return input("Enter your choice (1-4): ")


def view_conversations():
    clear_screen()
    conversations = get_conversations()
    if not conversations:
        print("You have no conversations yet.")
        input("Press Enter to continue...")
        return

    print("Your Conversations:")
    for idx, conv in enumerate(conversations, 1):
        participants = ", ".join(
            [
                user["username"]
                for user in conv["users"]
                if user["id"] != CURRENT_USER["id"]
            ]
        )
        print(f"{idx}. Conversation with: {participants}")

    choice = input(
        "\nEnter the number of the conversation to view messages (or 0 to go back): "  # noqa
    )
    if choice.isdigit() and 0 < int(choice) <= len(conversations):
        view_messages(conversations[int(choice) - 1]["id"])


def view_messages(conversation_id):
    clear_screen()
    messages = get_messages(conversation_id)
    for message in messages:
        sender = (
            "You"
            if message["sender_id"] == CURRENT_USER["id"]
            else f"User {message['sender_id']}"
        )
        print(f"{sender}: {message['content']}")
    input("\nPress Enter to go back...")


def send_new_message():
    clear_screen()
    conversations = get_conversations()
    if not conversations:
        print("You have no conversations. Create a new one.")
        participant_id = input(
            "Enter the user ID of the person you want to chat with: "
        )
        conversation = create_conversation(
            [CURRENT_USER["id"], int(participant_id)]
        )
        conversation_id = conversation["id"]
    else:
        print("Your Conversations:")
        for idx, conv in enumerate(conversations, 1):
            participants = ", ".join(
                [
                    user["username"]
                    for user in conv["users"]
                    if user["id"] != CURRENT_USER["id"]
                ]
            )
            print(f"{idx}. Conversation with: {participants}")

        choice = input(
            "\nEnter the number of the conversation to send a message (or 0 for a new conversation): "  # noqa
        )
        if choice == "0":
            participant_id = input(
                "Enter the user ID of the person you want to chat with: "
            )
            conversation = create_conversation(
                [CURRENT_USER["id"], int(participant_id)]
            )
            conversation_id = conversation["id"]
        elif choice.isdigit() and 0 < int(choice) <= len(conversations):
            conversation_id = conversations[int(choice) - 1]["id"]
        else:
            print("Invalid choice.")
            input("Press Enter to continue...")
            return

    content = input("Enter your message: ")
    send_message(conversation_id, content)
    print("Message sent successfully!")
    input("Press Enter to continue...")


def main():
    login_or_create_user()
    while True:
        choice = display_menu()
        if choice == "1":
            view_conversations()
        elif choice == "2":
            send_new_message()
        elif choice == "3":
            print("Logging out...")
            login_or_create_user()
        elif choice == "4":
            print("Thank you for using the Messaging App. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            time.sleep(2)


if __name__ == "__main__":
    main()
