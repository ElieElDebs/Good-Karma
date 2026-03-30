import os

from dotenv import load_dotenv
from fastapi import FastAPI

import App.Database.qdrant as qdrant
from Routes import search
from Routes import subreddits

print("Loading environment variables...")
load_dotenv("./Configuration/.env")

print("Initializing Qdrant and Model...")
qdrant.initialize_qdrant(
    host=os.getenv("QDRANT_HOST", "localhost"), port=int(os.getenv("QDRANT_PORT", 6333))
)
qdrant.initialize_model()
print("Qdrant and Model initialized.")

app = FastAPI()

app.include_router(search.router)
app.include_router(subreddits.router)


@app.get("/")
def read_root():
    return {
        "status": 200,
        "message": "Morlana API is running.",
        "version": {"api": "0.2.2", "name": "Morlana", "developer": "ArduiPie"},
    }
