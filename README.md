# Multi-Agentic Recruitment System

An AI-powered recruitment system that automates the process of job description analysis, CV matching, and interview scheduling.

## Features

- Job Description Summarizer: Analyzes and extracts key requirements from job descriptions
- Recruiting Agent: Matches candidate CVs with job requirements
- Shortlisting System: Automatically shortlists candidates based on match scores
- Interview Scheduler: Manages interview scheduling and communication

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- Git
- Ollama (for running LLMs locally)

## Installation Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd multiagentic-interview-system
```

2. **Create and activate a virtual environment**
```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up Ollama**
```bash
# Install Ollama from https://ollama.ai/
# After installation, pull the required models:
ollama pull llama2
ollama pull nomic-embed-text
```

5. **Initialize the database**
```bash
# The database will be automatically created when you first run the application
# It will be created as recruitment.db in your project directory
```

## Running the Application

1. **Start the Ollama server**
```bash
# Open a new terminal window and run:
ollama serve
```

2. **Start the FastAPI application**
```bash
# In your project directory, with the virtual environment activated:
uvicorn app.main:app --reload
```

3. **Access the API**
- The API will be available at: http://localhost:8000
- API documentation (Swagger UI) will be available at: http://localhost:8000/docs
- Alternative API documentation (ReDoc) will be available at: http://localhost:8000/redoc

## Testing the System

1. **Create a job posting**
```bash
curl -X POST "http://localhost:8000/jobs/" \
     -H "Content-Type: application/json" \
     -d '{
           "title": "Software Engineer",
           "company": "Tech Corp",
           "description": "Looking for a skilled software engineer...",
           "requirements": "5+ years of experience in Python..."
         }'
```

2. **Submit a candidate**
```bash
curl -X POST "http://localhost:8000/candidates/" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "John Doe",
           "email": "john@example.com",
           "cv_text": "Experienced software engineer...",
           "job_id": 1
         }'
```

3. **Schedule an interview**
```bash
curl -X POST "http://localhost:8000/interviews/" \
     -H "Content-Type: application/json" \
     -d '{
           "candidate_id": 1,
           "job_id": 1
         }'
```

## Troubleshooting

1. **Ollama Connection Issues**
- Ensure Ollama is running: `ollama serve`
- Check if models are downloaded: `ollama list`
- Verify Ollama API is accessible: `curl http://localhost:11434/api/tags`

2. **Database Issues**
- If you need to reset the database, delete the `recruitment.db` file
- The database will be recreated when you restart the application

3. **API Connection Issues**
- Ensure the FastAPI server is running
- Check if the port 8000 is available
- Verify all dependencies are installed correctly

## Technology Stack

### Core Framework & API
- FastAPI (v0.104.0+) - Modern, fast web framework for building APIs
- Uvicorn - ASGI server for running the FastAPI application
- Pydantic (v2.4.2+) - Data validation and settings management

### Language Models & AI
- Ollama (v0.1.6+) - Self-hosted LLM framework
  - llama2 - For general language processing tasks
  - nomic-embed-text - For text embeddings and semantic similarity
- LangChain (v0.1.0+) - Framework for building LLM applications
  - langchain-core (v0.1.10+)
  - langchain-community (v0.0.10+)

### Database
- SQLite - Lightweight, file-based database
- SQLAlchemy (v2.0.0+) - SQL toolkit and ORM
- Database Models:
  - JobDescription
  - Candidate
  - Interview

### Web & Data Processing
- Requests (v2.31.0+) - HTTP library for API calls
- BeautifulSoup4 (v4.12.2+) - Web scraping capabilities
- Python-multipart - For handling file uploads

### Development Tools
- python-dotenv - Environment variable management
- Type hints and annotations throughout the codebase

## Architecture

The system follows a multi-agent pattern with three main agents:

1. **Job Summarizer Agent**
   - Uses llama2 for analyzing job descriptions
   - Extracts key requirements and qualifications

2. **Recruiting Agent**
   - Combines llama2 and nomic-embed-text
   - Performs CV matching and scoring
   - Provides detailed match analysis

3. **Interview Scheduler Agent**
   - Uses llama2 for generating communications
   - Manages interview scheduling
   - Generates personalized interview invitations

## Project Structure

```
├── app/
│   ├── agents/           # Agent implementations
│   ├── models/          # Database models
│   ├── tools/           # Custom tools
│   ├── utils/           # Utility functions
│   └── main.py          # FastAPI application
├── tests/               # Test files
├── requirements.txt     # Project dependencies
└── README.md           # Project documentation
```

## API Endpoints

- `POST /jobs/`: Create a new job posting
- `POST /candidates/`: Process a candidate's CV
- `POST /interviews/`: Schedule an interview
- `GET /jobs/{job_id}/candidates`: Get all candidates for a job 