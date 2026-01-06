# AI Travel Planner

An intelligent AI-powered travel planning application that creates personalized trip itineraries using LangGraph agents and real-time data from multiple sources.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red?logo=streamlit)
![LangGraph](https://img.shields.io/badge/LangGraph-Latest-purple)

## Features

- **Destination Discovery** - Explore attractions, restaurants, and hidden gems using Google Places API
- **Weather Intelligence** - Real-time weather data for optimal trip planning
- **Budget Planning** - Smart expense calculations with currency conversion
- **Day-by-Day Itineraries** - Comprehensive travel plans tailored to your preferences
- **Multi-Provider LLM Support** - Works with Groq, OpenAI, and other providers

## Architecture

```
┌─────────────────┐     ┌─────────────────┐
│   Streamlit UI  │────▶│  FastAPI Backend │
└─────────────────┘     └────────┬────────┘
                                 │
                        ┌────────▼────────┐
                        │  LangGraph Agent │
                        └────────┬────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
┌───────▼───────┐  ┌─────────────▼──────────┐  ┌─────────▼─────────┐
│ Weather Tool  │  │  Place Search Tool     │  │ Currency/Expense  │
│ (OpenWeather) │  │ (Google Places/Tavily) │  │     Tools         │
└───────────────┘  └────────────────────────┘  └───────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.11+
- API Keys:
  - Groq API Key (or OpenAI)
  - Google Places API Key
  - Tavily API Key (optional, fallback search)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Tushar7012/AI-TRIP-PLANNER.git
   cd AI-TRIP-PLANNER
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

### Running Locally

1. **Start the FastAPI backend**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

2. **Start the Streamlit frontend** (new terminal)
   ```bash
   streamlit run app.py
   ```

3. Open http://localhost:8501 in your browser

## Deployment on Render

### Using Render Blueprint

1. Fork this repository to your GitHub account
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click **New** → **Blueprint**
4. Connect your GitHub repository
5. Render will automatically detect `render.yaml` and create both services
6. Add environment variables in the Render dashboard:
   - `GROQ_API_KEY`
   - `GPLACES_API_KEY`
   - `TAVILY_API_KEY` (optional)

### Manual Deployment

**Backend (FastAPI)**:
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Frontend (Streamlit)**:
- Build Command: `pip install -r requirements.txt`
- Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
- Environment Variable: `BACKEND_URL=https://your-api-service.onrender.com`

## API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/docs` | Swagger documentation |
| POST | `/query` | Generate travel plan |

### Query Request

```json
{
  "question": "Plan a 5-day trip to Tokyo with a budget of $2000"
}
```

## Project Structure

```
AI-TRIP-PLANNER/
├── agent/
│   └── agent_workflow.py    # LangGraph agent definition
├── config/
│   └── config.yaml          # LLM configuration
├── prompt_library/
│   └── prompt.py            # System prompts
├── tools/
│   ├── weather_info_tool.py
│   ├── place_search_tool.py
│   ├── expense_calculator_tool.py
│   └── currency_conversion.py
├── utils/
│   ├── model_loader.py
│   ├── weather_info.py
│   └── place_info_search.py
├── app.py                   # Streamlit frontend
├── main.py                  # FastAPI backend
├── render.yaml              # Render deployment config
├── Procfile                 # Alternative deployment
└── requirements.txt
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes | Groq API key for LLM |
| `GPLACES_API_KEY` | Yes | Google Places API key |
| `TAVILY_API_KEY` | No | Tavily search API key |
| `OPENAI_API_KEY` | No | OpenAI API key (alternative) |
| `BACKEND_URL` | Production | Backend API URL for frontend |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Tushar Das** - [GitHub](https://github.com/Tushar7012)