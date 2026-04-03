
---

**Developed by Elie El Debs**
<p align="center">
   <img src="../images/transparent-logo.png" alt="Good Karma logo" width="140" />
</p>

# Morlana Backend

Morlana Backend is the core API and analysis engine for the Good Karma project. It provides Reddit post analysis, semantic search, and subreddit management via a FastAPI service, leveraging a Qdrant vector database for similarity search.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Usage](#api-usage)
- [Qdrant Knowledge Base](#qdrant-knowledge-base)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Reddit post analysis**: Extracts KPIs and provides actionable advice for Reddit drafts.
- **Semantic search**: Finds similar posts using Qdrant vector search.
- **Subreddit management**: Handles subreddit metadata and targeting.
- **REST API**: Exposes endpoints for analysis, search, and subreddit operations.
- **FastAPI**: Modern, async Python backend with auto-generated docs.

## Architecture

```
User
   |
   v
Frontend (Next.js)
   |
   v
Morlana Backend (FastAPI)
   |
   v
Qdrant (Vector DB)
```

**Key modules:**

- `app.py`: FastAPI entrypoints
- `app_manual.py`: Script that populate the Qdrant client based on Workflow config file
- `App/Database/qdrant.py`: Qdrant client and DB logic
- `App/Middleware/`: Business logic (search, subreddit, etc.)
- `App/Utils/`: KPI, scoring, Reddit API, utilities
- `Routes/`: API route definitions
- `Configuration/`: App and workflow configs

**Data flow:**
1. User submits a Reddit draft via the frontend.
2. Backend analyzes the draft, computes KPIs, and queries Qdrant for similar posts.
3. Results (KPIs, advice, similar posts) are returned to the frontend.

## Installation

### Prerequisites

- Python 3.10+
- [Qdrant](https://qdrant.tech/) running locally or via Docker
- (Optional) Docker & Docker Compose

### Local Setup

```bash
# Clone the repository (from the root)
git clone https://github.com/yourusername/good_karma.git
cd good_karma/Morlana_backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Docker

You can run the backend and Qdrant using Docker Compose from the project root:

```bash
docker-compose up --build
```

This will start Qdrant, the backend, and the frontend (see main README for details).

## Quick Start

### Run Backend Only

```bash
# Ensure Qdrant is running (see below for DB setup)
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`.

### Healthcheck

Test the backend is running:

```bash
curl http://localhost:8000/
```

## API Usage

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Reddit draft analysis**: `POST /search`
- **Subreddit management**: `GET/POST /subreddits`
- **Healthcheck**: `GET /`

Example request:

```bash
curl -X POST "http://localhost:8000/search" -H "Content-Type: application/json" -d '{"title": "My Reddit post", "body": "Post content..."}'
```

See the interactive docs for full endpoint details and schemas.

## Qdrant Knowledge Base

The backend requires a populated Qdrant collection for semantic search. By default, the collection must exist and be filled with Reddit post embeddings.

### Options for Setup

1. **Populate via Reddit API**: Use the provided scripts to fetch and embed posts (requires Reddit developer credentials filled in the `.env` file in the config space).
2. **Import a pre-built collection**: If provided, download the Qdrant export and place it in `qdrant_storage/` as documented. Run the import script if available.

> **Note:** Providing a sample Qdrant collection lowers the barrier for new users. Ensure no sensitive data is included.

### Qdrant Management

- Collection config: `qdrant_storage/collections/morlana_collection/`
- Storage volume: `qdrant_storage/`
- See [Qdrant docs](https://qdrant.tech/documentation/) for manual management.


## Contributing

Contributions are welcome! Please:

1. Open an issue for bugs or feature requests.
2. Fork the repo and create a feature branch.
3. Keep pull requests focused and well-documented.
4. Follow code style and update documentation as needed.

## License

This project is licensed under the GNU Affero General Public License v3.0. See [../LICENSE](../LICENSE) for details.
