# Morlana Backend

Morlana is a backend API for Reddit post analysis, embedding, and KPI calculation using FastAPI, Qdrant, and NLP models.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Qdrant Setup (Docker)](#qdrant-setup-docker)
- [Remplissage de la base de connaissance Qdrant](#remplissage-de-la-base-de-connaissance-qdrant)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features

- Fetch Reddit posts and analyze their KPIs.
- Store and search embeddings using Qdrant vector database.
- FastAPI-based REST API.
- NLP preprocessing and sentiment analysis.

## Prerequisites

- Python 3.9+
- [Docker](https://www.docker.com/get-started)
- [Git](https://git-scm.com/)
- Reddit API credentials (client ID, client secret, user agent)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/morlana_backend.git
   cd morlana_backend
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Environment Variables:**

   Edit the `.env` file in `Configuration/.env` to set your database and Qdrant configuration:

   ```
   QDRANT_HOST = localhost
   QDRANT_PORT = 6333
   ```

2. **Reddit API Credentials:**

   You will need to provide your Reddit API credentials when initializing the Reddit fetcher in your scripts.

## Qdrant Setup (Docker)

1. **Install Docker:**

   Download and install Docker from [here](https://www.docker.com/get-started).

2. **Create a Docker network (recommended):**

   To allow containers to communicate (for example, if you add a database later), create a Docker network:

   ```bash
   docker network create morlana-net
   ```

3. **Pull the Qdrant Docker image:**

   ```bash
   docker pull qdrant/qdrant
   ```

4. **Run Qdrant:**

   ```bash
   docker run -p 6333:6333 -p 6334:6334 -v "$(pwd)/qdrant_storage:/qdrant/storage:z" --network morlana-net --name qdrant-db qdrant/qdrant
   ```

   This will start Qdrant on `localhost:6333`.

## Remplissage de la base de connaissance Qdrant

La base de connaissance Qdrant est vide lors de la première utilisation.  
Pour créer la collection et remplir la base avec des données issues de Reddit :

1. **Créer la collection Qdrant et lancer le remplissage**  
   Exécutez le script suivant :

   ```bash
   python app_manual.py
   ```

   Ce script va :
   - Créer la collection dans Qdrant si elle n'existe pas.
   - Récupérer les posts Reddit selon la configuration.
   - Ajouter les embeddings dans la base Qdrant.

2. **Vérifiez que la base est bien remplie avant d'utiliser l'API pour la recherche.**

## Running the Project

1. **Start Qdrant (see above).**

2. **Start the FastAPI server:**

   ```bash
   uvicorn app:app --reload
   ```

   The API will be available at `http://localhost:8000`.

## API Endpoints

- `/` : Health check and API info.
- `/search` : Search embeddings (see `Routes/search.py`).
- `/subreddits` : Subreddit-related endpoints (see `Routes/subreddits.py`).
- `/docs` : Show the documentation of the API

Refer to the code and FastAPI docs for more details.

## Troubleshooting

- **Qdrant not running:** Ensure Docker is running and Qdrant is started.
- **Model download issues:** Check your internet connection for downloading NLP models.
- **Reddit API errors:** Verify your credentials and Reddit API limits.

## License

This project is licensed under the MIT License.

---

**Developed by ArduiPie**
