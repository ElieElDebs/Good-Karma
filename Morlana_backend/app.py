import os

from dotenv import load_dotenv

print("Loading environment variables...")
loaded = load_dotenv("./Configuration/.env")

if loaded == False:
    print("ERROR : Environnement variables has not been loaded succesffuly ! ")

import App.Database.qdrant as qdrant
from App.Utils.llm import init_client
from fastapi import FastAPI
from Routes import post, search, subreddits

print("Initializing Qdrant and Model...")
qdrant.initialize_qdrant(
    host=os.getenv("QDRANT_HOST", "localhost"), port=int(os.getenv("QDRANT_PORT", 6333))
)
qdrant.initialize_model()
print("Qdrant and Model initialized.")

print("Init Gen AI Model ....")
init_client()
print("Gen AI model Successfully Loaded")

app = FastAPI()

app.include_router(search.router)
app.include_router(subreddits.router)
app.include_router(post.router)


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
