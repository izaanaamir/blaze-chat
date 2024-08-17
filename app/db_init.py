from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
from app.database import engine
from alembic import command
from alembic.config import Config


def init_db():
    with engine.begin() as conn:
        # Check if the database exists
        try:
            conn.execute(text("SELECT 1"))
            print("Database already exists.")
        except ProgrammingError:
            # If the database doesn't exist, create it
            conn.execute(text("CREATE DATABASE blazechat"))
            print("Database created successfully.")

    # Run Alembic migrations
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    print("Database schema created successfully.")


if __name__ == "__main__":
    init_db()
