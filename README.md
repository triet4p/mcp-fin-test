# MCP-FIN-TEST: An AI Financial Agent

MCP-FIN-TEST is an AI-powered financial agent built on the Model-Context-Protocol (MCP) architectural philosophy. This project demonstrates how to create a modular, extensible financial assistant that can analyze stock prices and provide investment insights using multiple language models and external data sources.

## Features

- **Multi-LLM Support**: Seamlessly switch between Google Gemini and OpenAI models via environment configuration
- **Tool-Based Architecture**: Extensible design with specialized tools for different financial tasks
- **Redis-Backed Memory**: Persistent conversation history using Redis for production deployments
- **LangSmith Integration**: Built-in tracing and debugging capabilities for agent behavior analysis
- **Dockerized Setup**: Containerized architecture for easy deployment and scaling
- **Real-time Data**: Integration with Yahoo Finance for current stock prices
- **Advanced Analytics**: Connection to external ITAPIA microservice for comprehensive financial analysis

## Architecture Overview

The project follows a modular architecture with clearly separated components:

```
app/
├── agent/          # Agent factory and orchestration logic
├── api/            # FastAPI endpoints for health checks and interactions
├── core/           # Configuration and core application settings
├── llms/           # LLM provider factory and client management
├── memory/         # Memory backend implementations (Redis, in-memory)
├── prompts/        # System prompts and prompt loading utilities
├── schemas/        # Pydantic models for request/response validation
├── tools/          # Specialized tools for financial data retrieval
└── main.py         # Application entry point
```

### Service Interaction

- **MCP-FIN Agent**: The main FastAPI service that handles user interactions and orchestrates the AI agent
- **Redis**: Persistent memory backend for storing conversation history
- **ITAPIA**: External microservice for advanced financial analysis (must be deployed separately)

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd mcp-fin-test
   ```

2. **Create environment file**:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file to configure your API keys and service endpoints.

3. **Start the services**:
   ```bash
   docker-compose up --build
   ```

   This command will start both the Redis memory service and the main agent service.

## API Usage

Once the services are running, you can interact with the agent using the `/api/v1/interact` endpoint:

```bash
curl -X POST "http://localhost:8003/api/v1/interact" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_123",
    "message": "What is the current price of AAPL?"
  }'
```

## How to Contribute

We welcome contributions to improve MCP-FIN-TEST! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code follows PEP 8 standards and includes appropriate tests and documentation.