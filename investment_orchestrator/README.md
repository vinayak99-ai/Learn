# Investment Research Orchestrator

> **Security Note**: Version 1.0.1 includes critical security update for FastAPI ReDoS vulnerability (CVE). Always use the latest version.

## Overview

The Investment Research Orchestrator is a sophisticated system that uses LangChain and OpenAI to intelligently orchestrate multiple Java backend APIs, providing comprehensive investment research insights through natural language queries.

## Architecture

```
User Query (Natural Language)
    ↓
FastAPI Endpoint (/research)
    ↓
LangChain Agent (GPT-4)
    ↓
Tools (6 different tools)
    ↓
API Client (httpx async)
    ↓
Java Backend APIs
    ↓
Database / Data Sources
    ↓
Response (Insights & Analysis)
```

### Component Overview

1. **FastAPI Service**: RESTful API endpoints for investment queries
2. **LangChain Agent**: Intelligent orchestration using GPT-4
3. **Tool Layer**: 6 specialized tools wrapping backend APIs
4. **API Client**: Async HTTP client with caching and retry logic
5. **Java Backend**: Data layer providing asset information

## Features

### Core Capabilities

- 🤖 **Natural Language Processing**: Ask questions in plain English
- 📊 **Real-time Data**: Current prices, fundamentals, and analyst ratings
- 🔍 **Smart Screening**: Find assets matching complex criteria
- ⚖️ **Asset Comparison**: Side-by-side analysis of multiple assets
- 🚀 **Async Operations**: High-performance parallel data fetching
- 💾 **Intelligent Caching**: Reduces backend load with TTL-based cache
- 🔄 **Retry Logic**: Robust error handling and automatic retries

### Available Tools

1. **GetAssetPrice**: Current price, volume, and price changes
2. **GetAssetClassification**: Sector, industry, market cap
3. **GetAssetBaskets**: Find assets matching criteria
4. **GetAssetResearchData**: Fundamentals and analyst ratings
5. **CompareAssets**: Side-by-side asset comparison
6. **ScreenAssets**: Enriched screening with full data

## Prerequisites

- Python 3.11+
- Docker and Docker Compose (optional)
- OpenAI API key
- Java backend service (see reference implementation)

## Quick Start

### Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd investment_orchestrator
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment**:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY and JAVA_BACKEND_URL
```

### Running Locally

**Start the orchestrator service**:
```bash
cd src
uvicorn orchestrator:app --reload --host 0.0.0.0 --port 8000
```

**Access the API**:
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Running with Docker

**Build and start services**:
```bash
docker-compose up -d
```

**View logs**:
```bash
docker-compose logs -f python-orchestrator
```

**Stop services**:
```bash
docker-compose down
```

## API Endpoints

### 1. Health Check
```http
GET /health
```

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "backend_url": "http://localhost:8080"
}
```

### 2. Research (Natural Language)
```http
POST /research
Content-Type: application/json

{
  "query": "What's the current price of Apple?"
}
```

**Response**:
```json
{
  "query": "What's the current price of Apple?",
  "answer": "Apple (AAPL) is currently trading at $150.25, up 1.18% from yesterday's close..."
}
```

### 3. Compare Assets
```http
POST /compare
Content-Type: application/json

{
  "asset_ids": ["AAPL", "MSFT", "GOOGL"]
}
```

**Response**:
```json
{
  "comparison": "Comparison of 3 Assets:\n========\nAAPL:\n  Price: $150.25 (1.18%)\n..."
}
```

### 4. Screen Assets
```http
POST /screen
Content-Type: application/json

{
  "sector": "Technology",
  "market_cap": "Large",
  "price_range": "<100",
  "min_growth": 20,
  "limit": 10
}
```

**Response**:
```json
{
  "results": "Screening Results (5 assets found):\n..."
}
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `JAVA_BACKEND_URL` | Java backend base URL | `http://localhost:8080` |
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `LOG_LEVEL` | Logging level | `INFO` |
| `CACHE_DURATION_MINUTES` | Cache TTL in minutes | `5` |
| `MAX_CONCURRENT_REQUESTS` | Max parallel requests | `10` |
| `REQUEST_TIMEOUT_SECONDS` | Request timeout | `30` |

### Configuration File

The `src/config.py` module provides centralized configuration management with validation.

## Example Queries

See [examples/example_queries.md](examples/example_queries.md) for comprehensive examples.

**Simple Queries**:
- "What's the current price of Tesla?"
- "Tell me about Apple's sector and industry"
- "What's the P/E ratio of Microsoft?"

**Complex Queries**:
- "Find me high-growth tech stocks under $100"
- "Compare NVDA, AMD, and INTC across key metrics"
- "What tech stocks are trading below their sector average PE but growing faster than 25%?"

## Development

### Project Structure

```
investment_orchestrator/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Container definition
├── docker-compose.yml            # Multi-container setup
├── .env.example                  # Environment template
├── src/
│   ├── __init__.py
│   ├── orchestrator.py           # Main FastAPI app
│   ├── api_client.py             # HTTP client
│   ├── config.py                 # Configuration
│   └── tools/
│       ├── __init__.py
│       ├── price_tool.py
│       ├── classification_tool.py
│       ├── baskets_tool.py
│       ├── research_tool.py
│       ├── comparison_tool.py
│       └── screening_tool.py
├── tests/
│   ├── __init__.py
│   └── test_orchestrator.py      # Unit tests
├── examples/
│   └── example_queries.md        # Example queries
└── java_backend_reference/
    ├── AssetDataController.java  # Controller reference
    └── DTOs.java                  # Data models
```

### Running Tests

**Run all tests**:
```bash
pytest tests/ -v
```

**Run with coverage**:
```bash
pytest tests/ --cov=src --cov-report=html
```

**Run specific test**:
```bash
pytest tests/test_orchestrator.py::test_health_endpoint -v
```

### Adding New Tools

1. Create a new tool file in `src/tools/`
2. Implement the tool logic with async support
3. Wrap with `StructuredTool.from_function()`
4. Add to `src/tools/__init__.py`
5. Register in `orchestrator.py` agent creation

**Example**:
```python
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from ..api_client import api_client

class MyToolInput(BaseModel):
    param: str = Field(description="Parameter description")

async def my_tool_impl(param: str) -> str:
    # Tool implementation
    result = await api_client.some_method(param)
    return f"Result: {result}"

my_tool = StructuredTool.from_function(
    coroutine=my_tool_impl,
    name="MyTool",
    description="Tool description for LLM",
    args_schema=MyToolInput,
)
```

## Performance Considerations

### Caching

The system implements in-memory caching with TTL to reduce backend load:
- Default cache duration: 5 minutes
- Configurable via `CACHE_DURATION_MINUTES`
- Cache keys based on endpoint + parameters

### Batch Processing

Multiple assets can be fetched in parallel using `asyncio.gather`:
```python
results = await api_client.batch_fetch(
    asset_ids=["AAPL", "MSFT", "GOOGL"],
    fetch_func="get_asset_price"
)
```

### Rate Limiting

Semaphore-based rate limiting prevents overwhelming the backend:
- Configurable via `MAX_CONCURRENT_REQUESTS`
- Default: 10 concurrent requests

## Java Backend Integration

### Required Endpoints

The Java backend must implement these endpoints:

1. `POST /api/getAssetPrice`
2. `POST /api/getAssetClassification`
3. `POST /api/getAssetBaskets`
4. `POST /api/getAssetResearchData`

See `java_backend_reference/` for complete implementation examples.

### Request/Response Format

All endpoints use JSON with specific DTO structures. See `DTOs.java` for complete specifications.

## Troubleshooting

### Common Issues

**1. OpenAI API Key Error**
```
ValueError: OPENAI_API_KEY environment variable is required
```
**Solution**: Set your OpenAI API key in `.env` file

**2. Connection Refused to Java Backend**
```
APIClientError: Request failed: Connection refused
```
**Solution**: Ensure Java backend is running and `JAVA_BACKEND_URL` is correct

**3. Timeout Errors**
```
APIClientError: Request timeout
```
**Solution**: Increase `REQUEST_TIMEOUT_SECONDS` or check backend performance

**4. Rate Limiting**
```
Too many requests
```
**Solution**: Adjust `MAX_CONCURRENT_REQUESTS` or implement backoff

### Debugging

**Enable debug logging**:
```bash
export LOG_LEVEL=DEBUG
```

**Check service health**:
```bash
curl http://localhost:8000/health
```

**View Docker logs**:
```bash
docker-compose logs -f python-orchestrator
```

## Cost Estimates

### OpenAI API Usage

Approximate costs per query type:

| Query Type | Avg Tokens | Cost (GPT-4) |
|------------|------------|--------------|
| Simple price query | 500 | $0.015 |
| Classification query | 600 | $0.018 |
| Screening (10 assets) | 3000 | $0.090 |
| Comparison (3 assets) | 2000 | $0.060 |

**Cost Optimization Tips**:
1. Use caching to reduce duplicate queries
2. Implement response streaming for long analyses
3. Consider GPT-3.5-turbo for simpler queries
4. Set token limits in agent configuration

## Production Deployment

### Checklist

- [ ] Set strong `OPENAI_API_KEY`
- [ ] Configure production `JAVA_BACKEND_URL`
- [ ] Set appropriate cache duration
- [ ] Configure rate limits
- [ ] Set up monitoring and logging
- [ ] Implement health checks
- [ ] Set up SSL/TLS certificates
- [ ] Configure backup and recovery
- [ ] Implement API authentication
- [ ] Set up load balancing (if needed)

### Monitoring

Monitor these key metrics:
- Request rate and latency
- Cache hit ratio
- Backend API errors
- OpenAI API costs
- Memory usage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run tests and ensure they pass
6. Submit a pull request

## License

[Your License Here]

## Support

For issues and questions:
- GitHub Issues: [Repository Issues URL]
- Documentation: [Docs URL]
- Email: [Support Email]

## Acknowledgments

- LangChain for the orchestration framework
- OpenAI for GPT-4 capabilities
- FastAPI for the web framework
- httpx for async HTTP client
