# Morlana Backend

<p align="center">
   <img src="../images/transparent-logo.png" alt="Good Karma logo" width="140" />
</p>

<p align="center">
   <strong>FastAPI backend service for Good Karma Reddit post analysis platform</strong>
</p>

<p align="center">
   <img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="Python 3.10+" />
   <img src="https://img.shields.io/badge/fastapi-0.119%2B-009688.svg" alt="FastAPI 0.119+" />
   <img src="https://img.shields.io/badge/qdrant-latest-ff6b35.svg" alt="Qdrant Latest" />
   <img src="https://img.shields.io/badge/license-AGPL--3.0-blue.svg" alt="License: AGPL-3.0" />
</p>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Development](#development)
- [Data Ingestion](#data-ingestion)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

**Morlana Backend** is the core API and analysis engine for the Good Karma project. It provides:

- 📊 Reddit post analysis with KPI extraction (readability, sentiment, engagement)
- 🔍 Semantic search via Qdrant vector database
- 💬 Actionable advice generation for post improvement
- ⚡ High-performance async processing with FastAPI
- 🔐 API key-based authentication and security
- 📚 Auto-generated API documentation (Swagger UI)

The backend orchestrates:
1. **NLP Analysis** - Compute KPIs and engagement scores
2. **Semantic Search** - Find similar posts using embeddings
3. **Data Retrieval** - Manage subreddit metadata and context
4. **Security** - Authenticate requests and manage access

## Features

- ✅ **Reddit Draft Analysis** - Extract KPIs and provide actionable feedback
- ✅ **Semantic Search** - Find similar high-performing posts via Qdrant
- ✅ **Engagement Scoring** - Compare drafts against successful posts
- ✅ **KPI Extraction** - Readability, sentiment, structure, engagement metrics
- ✅ **Timing Recommendations** - Best posting times per subreddit
- ✅ **API Key Security** - X-API-Key authentication for endpoints
- ✅ **FastAPI** - Modern async Python framework with auto-generated docs
- ✅ **Docker Support** - Containerized for easy deployment
- ✅ **Scalable** - Designed for horizontal scaling with Qdrant

## Architecture

### System Diagram

```
┌─────────────────────────────────────────┐
│         Next.js Frontend                │
│         (Port 3000)                     │
└────────────────┬────────────────────────┘
                 │ HTTP REST API
                 │
┌────────────────▼────────────────────────┐
│       FastAPI Backend Service            │
│         (Port 8000)                     │
│                                          │
│  ┌──────────────────────────────────┐  │
│  │ Routes/                           │  │
│  │ ├─ /search (draft analysis)      │  │
│  │ ├─ /subreddits (metadata)        │  │
│  │ └─ /health (status check)        │  │
│  └──────────────────────────────────┘  │
│                                          │
│  ┌──────────────────────────────────┐  │
│  │ App/Middleware/                  │  │
│  │ ├─ search.py (KPI computation)   │  │
│  │ └─ subreddits.py (metadata mgmt) │  │
│  └──────────────────────────────────┘  │
│                                          │
│  ┌──────────────────────────────────┐  │
│  │ App/Utils/                        │  │
│  │ ├─ kpi.py (KPI extraction)       │  │
│  │ ├─ GlobalEngagementScore*.py     │  │
│  │ ├─ Reddit.py (PRAW integration)  │  │
│  │ ├─ utils.py (helpers)            │  │
│  │ └─ security.py (auth logic)      │  │
│  └──────────────────────────────────┘  │
│                                          │
│  ┌──────────────────────────────────┐  │
│  │ App/Database/                     │  │
│  │ └─ qdrant.py (vector DB client)  │  │
│  └──────────────────────────────────┘  │
└────────────────┬────────────────────────┘
                 │ Vector Search & Embeddings
                 │ (Sentence Transformers 768-dim)
┌────────────────▼────────────────────────┐
│    Qdrant Vector Database                │
│      (Port 6333 API, 6334 Web UI)       │
│                                          │
│  - Stores embedded Reddit posts          │
│  - Performs cosine similarity search     │
│  - Persistent storage via volumes        │
└─────────────────────────────────────────┘
```

### Data Flow

```
1. User submits draft (title, body, subreddits)
           ↓
2. Backend receives request & validates API key
           ↓
3. Compute KPIs:
   - Readability score (Flesch-Kincaid, etc.)
   - Sentiment analysis (TextBlob)
   - Structure analysis
   - Engagement metrics
           ↓
4. Generate embeddings using Sentence Transformers
           ↓
5. Query Qdrant for similar posts (cosine distance)
           ↓
6. Compute engagement scores for comparison
           ↓
7. Generate actionable advice
           ↓
8. Return analysis to frontend
```

## Prerequisites

- **Python 3.10+**
- **Qdrant 1.0+** (running instance required)
- **pip** or **conda** (package manager)
- **Docker** (optional, for containerized setup)

### System Requirements

- **Memory:** 4GB+ (for Sentence Transformers model)
- **Disk:** 5GB+ (for dependencies and Qdrant storage)
- **CPU:** Multi-core recommended (async processing)

## Installation

### Option 1: Docker (Recommended for Quick Setup)

```bash
# From repository root
docker-compose up backend
```

This automatically:
- Builds the backend container
- Pulls the Python 3.10 base image
- Installs all dependencies
- Downloads NLTK data
- Starts FastAPI on port 8000

### Option 2: Local Development Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/ElieElDebs/Good-Karma.git
cd Good-Karma/Morlana_backend
```

#### 2. Create Virtual Environment

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
# For CPU-only setup
pip install -r generic.txt

# For GPU support (NVIDIA CUDA)
pip install -r gpu.txt

# Note: Both can be installed together for mixed environments
# The Dockerfile installs both
```

#### 4. Download NLTK Data (Required)

```bash
python -m nltk.downloader stopwords punkt wordnet punkt_tab
```

These downloads are essential for:
- **stopwords:** Removing common words in KPI analysis
- **punkt:** Sentence tokenization for structure analysis
- **wordnet:** Semantic analysis and lemmatization
- **punkt_tab:** Enhanced tokenizer for better accuracy

#### 5. Configure Environment

```bash
# Copy example config
cp Configuration/.env.example Configuration/.env

# Edit with your settings
nano Configuration/.env  # or use your preferred editor
```

**Required Configuration:**

```env
# Qdrant Database (Required)
QDRANT_HOST = localhost
QDRANT_PORT = 6333
QDRANT_COLLECTION_NAME = morlana_collection
QDRANT_VECTOR_SIZE = 768
QDRANT_DISTANCE = cosine

# API Authentication (Required)
API_KEY = your_secure_api_key_here

# Reddit API (for data ingestion only)
client_id = your_reddit_app_id
client_secret = your_reddit_app_secret
user_agent = your_user_agent_string
```

**Important:** The `API_KEY` is required for all requests to the `/search` endpoint. It must be passed as the `X-API-Key` header.

#### 6. Start Qdrant (if not using Docker Compose)

```bash
# Option A: Docker container
docker run -d -p 6333:6333 -p 6334:6334 \
  -v qdrant_storage:/qdrant/storage \
  qdrant/qdrant

# Option B: Native installation (see Qdrant docs)
```

#### 7. Start Backend

```bash
# Development mode (with hot reload)
uvicorn app:app --reload

# Production mode
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at `http://localhost:8000`

## Configuration

### Environment Variables (`Configuration/.env`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `QDRANT_HOST` | Yes | `localhost` | Qdrant server hostname |
| `QDRANT_PORT` | Yes | `6333` | Qdrant API port |
| `QDRANT_COLLECTION_NAME` | Yes | - | Name of vector collection |
| `QDRANT_VECTOR_SIZE` | No | `768` | Embedding dimension (Sentence Transformers) |
| `QDRANT_DISTANCE` | No | `cosine` | Distance metric (cosine, euclidean, manhattan) |
| `API_KEY` | **Yes** | - | **API key for authentication (X-API-Key header)** |
| `client_id` | Conditional | - | Reddit API client ID (for ingestion) |
| `client_secret` | Conditional | - | Reddit API secret (for ingestion) |
| `user_agent` | Conditional | - | Reddit user agent string |

### Model Configuration

The backend uses **Sentence Transformers** for semantic embeddings:
- **Default Model:** `all-MiniLM-L6-v2` or similar 768-dimensional models
- **Embedding Dimension:** 768 (configurable via `QDRANT_VECTOR_SIZE`)
- **Distance Metric:** Cosine similarity (configurable)

To use a different model, edit `App/Database/qdrant.py` and update the `initialize_model()` function.

## Quick Start

### 1. Verify Setup

```bash
# Health check
curl http://localhost:8000/

# Expected response:
# {"status": 200, "message": "Morlana API is running.", "version": {...}}
```

### 2. Access API Documentation

Open your browser:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI Schema:** http://localhost:8000/openapi.json

### 3. Analyze a Reddit Draft

```bash
# With API key authentication (Required)
curl -H "X-API-Key: your_api_key_from_env" \
  "http://localhost:8000/search?title=My%20Post&body=Content&subreddits=r/test"

# Response includes:
# - KPIs (readability, sentiment, structure)
# - Engagement scores
# - Similar posts from Qdrant
# - Actionable advice

# Error if API key is missing:
# {"detail": "Forbidden - Missing or invalid API key"}
```

⚠️ **Note:** Replace `your_api_key_from_env` with the actual `API_KEY` value from your `.env` file.

## API Endpoints

### Health Check

```
GET /
```

Returns system status and version information.

**Response:**
```json
{
  "status": 200,
  "message": "Morlana API is running.",
  "version": {
    "api": "0.6.2",
    "name": "Morlana",
    "developer": "ArduiPie"
  }
}
```

### Analyze Reddit Draft

```
GET /search
```

**Authentication:** Requires `X-API-Key` header

**Query Parameters:**
- `title` (string, required): Post title/headline
- `body` (string, required): Post content/body
- `subreddits` (list[string], required): Target subreddits with `r/` prefix

**Example:**
```bash
curl -H "X-API-Key: your_key" \
  "http://localhost:8000/search?title=Check%20this%20out&body=Body%20content&subreddits=r/test&subreddits=r/AskReddit"
```

**Response:**
```json
{
  "status": 200,
  "kpis": {
    "readability_score": 65.2,
    "sentiment_score": 0.45,
    "structure_score": 0.78,
    ...
  },
  "engagement_score": "Good",
  "similar_posts": [
    {
      "title": "Similar post 1",
      "score": 0.89,
      "subreddit": "r/test"
    },
    ...
  ],
  "advice": [
    "Consider using shorter sentences for better readability",
    ...
  ],
  "best_posting_times": {
    "monday": "18:00-20:00",
    ...
  }
}
```

### Manage Subreddits

```
GET /subreddits
```

Lists available subreddits in the knowledge base.

```
POST /subreddits
```

Add or update subreddit metadata (requires JSON body).

### API Documentation

```
GET /docs
```

Interactive Swagger UI for testing endpoints.

```
GET /redoc
```

Alternative API documentation view.

## Project Structure

```
Morlana_backend/
│
├── app.py                          # Main FastAPI application
├── app_manual.py                   # Data ingestion script
│
├── Configuration/
│   ├── .env.example                # Example environment variables
│   ├── .env                        # Your configuration (not tracked)
│   └── workflow.json               # Data ingestion workflow config
│
├── Routes/
│   ├── search.py                   # POST /search endpoint
│   ├── subreddits.py               # GET/POST /subreddits endpoints
│   └── __init__.py
│
├── App/
│   ├── Database/
│   │   └── qdrant.py               # Qdrant client initialization
│   │
│   ├── Middleware/
│   │   ├── search.py               # Search logic & KPI orchestration
│   │   ├── subreddits.py           # Subreddit metadata logic
│   │   └── __init__.py
│   │
│   ├── Utils/
│   │   ├── kpi.py                  # KPI calculation functions
│   │   ├── GlobalEngagementScore.py
│   │   ├── GlobalEngagementScoreNew.py
│   │   ├── Reddit.py               # PRAW Reddit API wrapper
│   │   ├── security.py             # API key authentication
│   │   ├── utils.py                # Helper functions
│   │   └── __init__.py
│   │
│   ├── Scripts/
│   │   ├── post_fetching.py        # Fetch posts from Reddit
│   │   └── embeddings.py           # Generate embeddings
│   │
│   └── __init__.py
│
├── generic.txt                     # Python dependencies (CPU)
├── gpu.txt                         # Python dependencies (GPU)
├── Dockerfile                      # Container configuration
├── .dockerignore
└── readme.md                       # This file
```

## Development

### Running in Development Mode

```bash
# With hot reload
uvicorn app:app --reload

# Specify host and port
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Code Quality

```bash
# Format code with black
black .
black app.py  # Specific file

# Check formatting without changes
black --check .

# Format specific directory
black App/Utils/
```

### Adding New Endpoints

1. Create a new file in `Routes/` (e.g., `Routes/analysis.py`)
2. Define FastAPI router with endpoints
3. Import and register in `app.py`:

```python
from Routes import analysis
app.include_router(analysis.router)
```

4. Update API documentation in the endpoint docstring
5. Test with Swagger UI at `/docs`

### Modifying KPI Calculations

**Content-level metrics:**
- Edit `App/Utils/kpi.py` for readability, sentiment, structure

**Engagement scoring:**
- Edit `App/Utils/GlobalEngagementScore.py` for engagement algorithms
- Changes take effect on next `/search` request

**Helper functions:**
- Edit `App/Utils/utils.py` for posting times and other utilities

## Data Ingestion

### Prerequisites

- Reddit API credentials (client ID, client secret, user agent)
- Configured `.env` file with Reddit credentials

### Using app_manual.py

This script populates Qdrant from a configuration file:

```bash
python app_manual.py
```

**Workflow Configuration** (`Configuration/workflow.json`):

```json
{
  "subreddits": [
    {
      "name": "r/test",
      "limit": 100,
      "time_filter": "month"
    }
  ],
  "output_collection": "morlana_collection"
}
```

### Using post_fetching.py

For automated, continuous data collection:

```bash
python App/Scripts/post_fetching.py
```

Configure via environment variables:
- `SUBREDDITS` - Comma-separated list (e.g., `"r/test,r/AskReddit"`)
- `FETCH_LIMIT` - Posts to fetch per subreddit
- `REFRESH_INTERVAL` - How often to refresh data

### Ingestion Best Practices

1. **Start small:** Test with 1-2 subreddits and small limits
2. **Monitor Qdrant:** Check collection stats at `http://localhost:6334`
3. **Respect rate limits:** Reddit API has rate limiting; add delays between requests
4. **Update regularly:** Refresh data periodically for fresh search results
5. **Backup collections:** Export Qdrant collections before major updates

## Troubleshooting

### Qdrant Connection Error

**Error:** `Failed to connect to Qdrant at localhost:6333`

**Solutions:**
```bash
# 1. Verify Qdrant is running
curl http://localhost:6333/health

# 2. Check port is open
lsof -i :6333  # macOS/Linux
netstat -ano | findstr :6333  # Windows

# 3. Start Qdrant if not running
docker run -d -p 6333:6333 qdrant/qdrant

# 4. Check QDRANT_HOST and QDRANT_PORT in .env
cat Configuration/.env | grep QDRANT
```

### NLTK Data Missing

**Error:** `LookupError: Resource stopwords not found`

**Solution:**
```bash
python -m nltk.downloader stopwords punkt wordnet punkt_tab
```

### API Key Authentication Fails

**Error:** `403 Forbidden - Missing or invalid X-API-Key`

**Solutions:**
```bash
# 1. Verify API_KEY is configured
cat Configuration/.env | grep API_KEY

# 2. Ensure API_KEY is set to a non-empty value
API_KEY = your_secure_key_here

# 3. Pass API key in X-API-Key header
curl -H "X-API-Key: your_secure_key_here" \
  http://localhost:8000/search?title=Test&body=Content&subreddits=r/test

# 4. Verify key matches between backend (.env) and frontend (.env)
# They must be identical for successful authentication

# 5. Restart backend after changing API_KEY
uvicorn app:app --reload
```

**Debugging:**
```bash
# Check if security.py is correctly implementing authentication
cat App/Utils/security.py

# Enable debug logging (if available)
uvicorn app:app --reload --log-level debug
```

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Verify virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r generic.txt
```

### Sentence Transformers Model Download Hangs

**Issue:** First run downloads model (~500MB)

**Solutions:**
- Be patient; download may take minutes depending on internet
- Check disk space (5GB+ available)
- Pre-download model:
  ```bash
  python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
  ```

## Contributing

Contributions to the backend are welcome! Areas of focus:

- **KPI Improvements:** Better readability, sentiment, and engagement metrics
- **Performance:** Optimize search speed and API response times
- **Testing:** Add unit and integration tests
- **Deployment:** Production hardening, scaling, monitoring
- **Documentation:** Clearer code comments and guides

### Development Workflow

1. Create a feature branch
2. Make your changes
3. Format code: `black .`
4. Test locally with `uvicorn app:app --reload`
5. Submit a pull request with clear description

See [CLAUDE.md](../CLAUDE.md) and [CONTRIBUTING](../CONTRIBUTING.md) for more details.

## License

GNU Affero General Public License v3.0 (AGPL-3.0)

If you deploy a modified version as a network service, you must share your code. Read [LICENSE](../LICENSE) for details.

## Support

- **Issues:** https://github.com/ElieElDebs/Good-Karma/issues
- **Email:** elie.eldebs@outlook.fr
- **Documentation:** See [CLAUDE.md](../CLAUDE.md) for development guide

---

<p align="center">
  <strong>Built with ❤️ for the Good Karma community</strong>
  <br>
  <a href="https://github.com/ElieElDebs/Good-Karma">⭐ Star us on GitHub</a>
</p>
