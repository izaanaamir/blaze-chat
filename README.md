# BlazeChat: Real-time Messaging Application

BlazeChat is a real-time messaging application built with FastAPI, SQLAlchemy, and WebSockets. It allows users to create accounts, start conversations, send messages, and receive real-time updates.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Database Setup](#database-setup)
5. [Running the Application](#running-the-application)
6. [API Endpoints](#api-endpoints)
7. [Terminal Client](#terminal-client)
8. [Testing](#testing)


## Prerequisites

- Python 3.7+
- PostgreSQL
- pip (Python package manager)

## Installation

1. Clone the repository:
- git clone https://github.com/yourusername/blazechat.git
- cd blazechat

2. Create a virtual environment:
- python -m venv venv

3. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```

4. Install the required packages:
- pip install -r requirements.txt

## Configuration

1. Create a `.env` file in the root directory with the following content:
DATABASE_URL=postgresql://user:password@localhost/blazechat
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

Replace `user`, `password`, and `blazechat` with your PostgreSQL credentials and desired database name.

2. Generate a secret key:
python -c "import secrets; print(secrets.token_hex(32))"

Copy the output and replace `your_secret_key_here` in the `.env` file.

Add the Database URL to Alembic.ini

## Database Setup

1. Create the database:

createdb blazechat

2. Run the database migrations:

alembic upgrade head

## Running the Application

1. Start the FastAPI server:
uvicorn app.main:app --reload

## API Endpoints

- `POST /users/`: Create a new user
- `POST /token`: Login and get access token
- `GET /users/me`: Get current user information
- `POST /messages/conversations/`: Create a new conversation
- `GET /messages/conversations/`: Get user's conversations
- `POST /messages/conversations/{conversation_id}/messages/`: Send a message
- `GET /messages/conversations/{conversation_id}/messages/`: Get messages in a conversation


## Terminal Client

BlazeChat includes a terminal-based client for a more interactive messaging experience directly from your command line.

To use the terminal client:

1. Ensure the FastAPI server is running.

2. Open a new terminal window and navigate to the project directory.

3. Activate the virtual environment (if not already activated):
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`

4. Run the terminal client:
    - python terminal_client.py

5. Follow the prompts to:
- Log in or create a new account
- Start a new conversation or join an existing one
- Send and receive messages

### Terminal Client Features

- User authentication (login/registration)
- Create new conversations
- Join existing conversations
- Send and receive messages
- View message history

## Testing

To run the test suite:
pytest


## To be done:
-  Add real-time messaging functionality using webhooks
- User can also upload other media types
