# MCP Hosts - Financial Agent

This directory contains the implementation of the MCP Financial Agent, a modular, extensible financial assistant built on the Model-Context-Protocol (MCP) architectural philosophy.

## Project Structure

```
app/
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

## Documentation

- [Application Architecture](docs/APP_ARCHITECTURE.md) - Comprehensive overview of the application architecture
- [Agent Module](docs/AGENT_MODULE.md) - Details about the agent core functionality
- [LLM Module](docs/LLM_MODULE.md) - Information about language model support and configuration
- [Tools Module](docs/TOOLS_MODULE.md) - Explanation of dynamic tool discovery and creation
- [Memory Module](docs/MEMORY_MODULE.md) - Details about conversation history management

## Key Features

- **Multi-LLM Support**: Seamlessly switch between Google Gemini, OpenAI, OpenRouter, and Ollama models
- **Dynamic Tool Discovery**: Automatically discover and integrate tools from MCP Servers registry
- **Pluggable Memory**: Support for both in-memory and Redis-backed conversation history
- **Configurable Prompts**: YAML-based prompt management system
- **Caching Support**: Optional Redis caching for LLM responses

## Environment Configuration

The application is configured through environment variables. See `.env.example` for required variables.