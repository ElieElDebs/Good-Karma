import yaml
import os

from dotenv import load_dotenv

from App.Scripts.post_fetching import init_reddit_fetcher, call_fetching_pipeline

# Load .env file for environment variables
load_dotenv("Configuration/.env")

# Load workflow Configuration
with open("Configuration/workflow.yaml", "r") as workflow_file:
    workflow_config = yaml.safe_load(workflow_file)


# Init Qdrant
from App.Database.qdrant import initialize_qdrant, initialize_model

print("Initializing Qdrant and Model...")
initialize_qdrant()
initialize_model()
print("Qdrant and Model initialized.")

# ========================= Subreddit Post Fetching and Embedding Addition ========================= #
if workflow_config.get("fetch_reddit_posts", {}).get("enabled", False):

    print("Starting subreddit post fetching and embedding addition...")

    # Initialize Reddit Fetcher
    FETCHER = init_reddit_fetcher(
        reddit_id=os.getenv("client_id"),
        reddit_secret=os.getenv("client_secret"),
        reddit_user_agent=os.getenv("user_agent"),
    )

    # Call Fetching Pipeline
    treshold_configuration = workflow_config["fetch_reddit_posts"]["subreddits"]

    call_fetching_pipeline(
        treshold_configuration=treshold_configuration,
        collection_name=os.getenv("QDRANT_COLLECTION_NAME"),
    )

    print("Subreddit post fetching and embedding addition completed.")
