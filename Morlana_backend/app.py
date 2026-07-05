import os
from dotenv import load_dotenv

print("Loading environment variables...")
loaded = load_dotenv("./Configuration/.env")

if loaded == False:
    print("ERROR : Environnement variables has not been loaded succesffuly ! ")

from fastapi import FastAPI

import App.Database.qdrant as qdrant
from Routes import search, subreddits

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
    """
    Main
    """
    return {
        "status": 200,
        "message": "Morlana API is running.",
        "version": {"api": "0.6.2", "name": "Morlana", "developer": "ArduiPie"},
    }
