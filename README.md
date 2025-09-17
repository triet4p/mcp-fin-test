# MCP-FIN-TEST: An AI Financial Agent

MCP-FIN-TEST is an AI-powered financial agent built on the Model-Context-Protocol (MCP) architectural philosophy. This project demonstrates how to create a modular, extensible financial assistant that can analyze stock prices and provide investment insights using multiple language models and external data sources.

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Project Structure](#project-structure)
- [Services](#services)
- [Setup and Installation](#setup-and-installation)
- [API Usage](#api-usage)
- [Documentation](#documentation)
- [Citation](#citation)

## Features

- **Multi-LLM Support**: Seamlessly switch between Google Gemini, OpenAI, OpenRouter, and Ollama models via environment configuration
- **Tool-Based Architecture**: Extensible design with specialized tools for different financial tasks
- **Pluggable Memory**: Support for both in-memory and Redis-backed conversation history
- **LangSmith Integration**: Built-in tracing and debugging capabilities for agent behavior analysis
- **Dockerized Setup**: Containerized architecture for easy deployment and scaling
- **Real-time Data**: Integration with Yahoo Finance for current stock prices
- **Advanced Analytics**: Connection to external ITAPIA microservice for comprehensive financial analysis
- **Dynamic Tool Discovery**: Automatic discovery of tools from MCP Servers registry
- **Configurable Prompts**: YAML-based prompt management system
- **Caching Support**: Optional Redis caching for LLM responses

## Architecture Overview

The project follows a microservices architecture with clearly separated components:

```
mcp-fin-test/
├── mcp_hosts/        # Main AI financial agent service
├── mcp_servers/      # Tool registry service
├── yf/               # Yahoo Finance real-time price service
├── docker-compose.yml # Orchestration for all services
└── README.md         # This file
```

### Component Services

1. **MCP Hosts** (`mcp_hosts/`): The main AI financial agent service
2. **MCP Servers** (`mcp_servers/`): Tool registry service that provides tool specifications
3. **YF Service** (`yf/`): Yahoo Finance real-time price service
4. **ITAPIA**: An external projects, use to give full analysis and advisor to personal investment. Please check:
   [triet4p/itapia](https://github.com/triet4p/itapia.git)

## Project Structure

### MCP Hosts (Main Agent)

The main AI financial agent service built with FastAPI and LangChain:

```
mcp_hosts/app/
├── agent/          # Agent factory and orchestration logic
├── api/            # FastAPI endpoints for health checks and interactions
├── clients/        # Tools discovery and external service clients
├── core/           # Configuration and core application settings
├── llms/           # LLM provider factory and client management
├── memory/         # Memory backend implementations (Redis, in-memory)
├── mcp_schemas/    # Auto-generated Pydantic models for external services
├── prompts/        # System prompts and prompt loading utilities
├── schemas/        # Pydantic models for request/response validation
└── main.py         # Application entry point
```

### MCP Servers (Tool Registry)

The tool registry service that provides tool specifications to agent hosts:

```
mcp_servers/app/
├── api/            # FastAPI endpoints for tools and providers
├── core/           # Configuration and core application settings
├── spec/           # Tool and provider specifications (YAML)
├── dependencies.py # Configuration loading and caching
└── main.py         # Application entry point
```

### YF Service (Yahoo Finance)

The Yahoo Finance real-time price service:

```
yf/app/
├── api/            # FastAPI endpoints for health checks and price data
├── core/           # Configuration and core application settings
├── tools/          # Business logic for fetching data from Yahoo Finance
├── schemas.py      # Pydantic models for data validation
└── main.py         # Application entry point
```

## Services

### MCP Hosts (Main Agent)

The main FastAPI service that handles user interactions and orchestrates the AI agent:

- **Port**: 8005
- **Health Check**: `GET /api/v1/health`
- **Interaction**: `POST /api/v1/interact`

### MCP Servers (Tool Registry)

The service that provides tool specifications to agent hosts:

- **Port**: 8003
- **Health Check**: `GET /api/v1/health`
- **Tools**: `GET /api/v1/tools`
- **Providers**: `GET /api/v1/providers`

### YF Service (Yahoo Finance)

The service that provides real-time stock price data:

- **Port**: 8004
- **Health Check**: `GET /api/v1/health`
- **Real-time Price**: `GET /api/v1/market/tickers/{ticker}/price/realtime`

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd mcp-fin-test
   ```

2. **Create environment files**:
   ```bash
   cp ./mcp_host/.env.example ./mcp_hosts/.env
   cp ./mcp_servers/.env.example ./mcp_servers/.env
   cp ./yf/.env.example ./yf/.env
   ```
   Edit the `.env` files to configure your API keys and service endpoints.

3. **Start the services**:
   ```bash
   rebuild-all.cmd
   docker-compose up -d
   ```

   This command will start all services including:
   - Redis memory service
   - Main agent service (MCP Hosts)
   - Tool registry service (MCP Servers)
   - Yahoo Finance service (YF)

4 **Start ITAPIA**:
   If you want MCP use ITAPIA tools, please run repo [triet4p/itapia](https://github.com/triet4p/itapia.git).
   You can see how to install and run this external repo in Docker.

## API Usage

### Interacting with the Agent

Once the services are running, you can interact with the agent using the `/api/v1/interact` endpoint:

```bash
curl -X POST "http://localhost:8005/api/v1/interact" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session_123",
    "message": "What is the current price of AAPL?"
  }'
```

### Getting Real-time Stock Prices

You can also directly query the Yahoo Finance service:

```bash
curl -X GET "http://localhost:8004/api/v1/market/tickers/AAPL/price/realtime"
```

### Discovering Available Tools

Agent hosts can discover available tools from the MCP Servers:

```bash
curl -X GET "http://localhost:8003/api/v1/tools"
```

## Documentation

Each module has its own detailed documentation:

### Main Agent (MCP Hosts)
- [Overview](mcp_hosts/README.md)
- [Architecture Overview](mcp_hosts/docs/APP_ARCHITECTURE.md)
- [Agent Module](mcp_hosts/docs/AGENT_MODULE.md)
- [LLM Module](mcp_hosts/docs/LLM_MODULE.md)
- [Tools Module](mcp_hosts/docs/TOOLS_MODULE.md)
- [Memory Module](mcp_hosts/docs/MEMORY_MODULE.md)
- [Schemas Module](mcp_hosts/docs/SCHEMAS_MODULE.md)

### Tool Registry (MCP Servers)
- [Overview](mcp_servers/README.md)
- [Tools Module](mcp_servers/docs/TOOLS_MODULE.md)
- [Providers Module](mcp_servers/docs/PROVIDERS_MODULE.md)

### Yahoo Finance Service (YF)
- [Overview](yf/README.md)
- [Real-time Price Module](yf/docs/REALTIME_MODULE.md)

## Citation

If you use this project or reference its concepts, please cite the following thesis:

[Le, Minh Triet]. (2025). *ITAPIA: An Intelligent and Transparent AI-Powered Personal Investment Assistant*. Graduate Thesis, Hanoi University of Science and Technology, Vietnam.