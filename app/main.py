from fastapi import FastAPI, BackgroundTasks
from app.api.endpoints import users, auth
from .database import Base, engine
from .db_init import init_db
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, tags=["authentication"])
app.include_router(users.router, prefix="/users", tags=["users"])


@app.get("/")
def read_root():
    return {"message": "Welcome to BlazeChat API"}


@app.post("/init-db")
async def initialize_database(background_tasks: BackgroundTasks):
    background_tasks.add_task(init_db)
    return {
        "message": "Database initialization started. This may take a moment."
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
