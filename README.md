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
- 

## Architecture and Design Choices

### Why I Implemented It This Way

1. **FastAPI Framework**
   - Fast performance: FastAPI is built on Starlette and Pydantic, offering high performance.
   - Type checking: FastAPI's use of Python type hints provides better code quality and reduces runtime errors.

2. **SQLAlchemy ORM**
   - Powerful querying: Provides a pythonic way to construct complex database queries.

3. **WebSockets for Real-time Communication [TO BE IMPLEMENTED]**
   - Instant updates: Allows for real-time message delivery without polling.
   - Efficient: Reduces server load compared to frequent HTTP requests.
   - Bi-directional: Enables both server-to-client and client-to-server real-time communication.

4. **JWT for Authentication**
   - Stateless: No need to store session information on the server.
   - Scalable: Works well in distributed systems and microservices architectures.
   - Secure: When implemented correctly, provides a robust authentication mechanism.

5. **Alembic for Database Migrations**
   - Version control for database schema: Allows tracking and managing database changes over time.
   - Easy rollbacks: Provides the ability to revert database changes if needed.

6. **Terminal Client**
   - Ease of testing: Allows developers to quickly test the application without a full GUI.
   - Accessibility: Provides a way to use the application in environments where a GUI is not available or preferred.
   - Demonstrates WebSocket usage: Serves as a practical example of implementing real-time features.

7. **Modular Structure**
   - Separation of concerns: Keeps different aspects of the application (models, schemas, CRUD operations) separate for better organization.
   - Scalability: Makes it easier to add new features or modify existing ones without affecting the entire codebase.
   - Testability: Allows for more focused and efficient unit testing.

8. **Environment Variables for Configuration**
   - Security: Keeps sensitive information like database credentials out of the codebase.
   - Flexibility: Allows for easy configuration changes between different environments (development, staging, production).

9. **Comprehensive Testing Suite**
   - Reliability: Ensures that the application behaves as expected and helps catch regressions.
   - Documentation: Tests serve as a form of documentation, showing how different parts of the system should work.
   - Confidence in refactoring: Makes it safer to make changes to the codebase.

These design choices were made for using a modern backend framework in combination with some tools like Pydantic as well as SQLAchemy and Alembic, the backend takes care of authentication for users as well as ensuring that conversations are displayed correctly. This appliacation takes care of all the important APIs. 
