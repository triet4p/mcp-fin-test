# MCP Financial Agent - Application Architecture

This document provides a comprehensive overview of the MCP Financial Agent's architecture, explaining the key modules and their interactions.

## Overview

The MCP Financial Agent is a modular, extensible financial assistant built on the Model-Context-Protocol (MCP) architectural philosophy. It leverages multiple language models and external data sources to provide investment insights and financial analysis.

## Core Modules

### 1. Agent (`app/agent`)

The Agent module is the core of the financial assistant. It orchestrates the interaction between the user, the language model, and the available tools.

Key components:
- **Agent Factory** (`_factory.py`): Creates and configures the LangChain agent with tools, prompts, and memory management
- **Agent Executor**: Manages the agent's execution loop, handling tool calling and response generation

The agent uses a system prompt that defines its behavior as a professional, friendly Vietnamese-speaking financial assistant.

### 2. Core Configuration (`app/core`)

The Core module handles application configuration through environment variables.

Key features:
- LLM provider configuration (Google, OpenAI, OpenRouter, Ollama)
- API key management
- Memory backend selection (in-memory or Redis)
- Caching configuration
- Prompt file and system prompt ID settings

### 3. Language Models (`app/llms`)

The LLMs module provides a factory pattern implementation for creating language model clients.

Supported providers:
- **Google**: Google Gemini models
- **OpenAI**: OpenAI GPT models
- **OpenRouter**: Various models via the OpenRouter API
- **Ollama**: Local models via Ollama

Features:
- Dynamic LLM client creation based on configuration
- Optional Redis caching for LLM responses

### 4. Memory Management (`app/memory`)

The Memory module handles conversation history storage with support for multiple backends.

Supported backends:
- **In-Memory**: Temporary storage in application memory (development/testing)
- **Redis**: Persistent storage using Redis (production)

The factory pattern allows switching between backends through configuration without changing code.

### 5. Tools Discovery (`app/clients`)

The Tools Discovery module dynamically discovers and creates tools that the agent can use.

Process:
1. Connects to the MCP Servers registry to fetch tool specifications
2. Dynamically imports required Pydantic schemas
3. Creates LangChain tools from specifications
4. Makes tools available to the agent

This enables the agent to use external services without hardcoding tool definitions.

### 6. Prompt Management (`app/prompts`)

The Prompt module handles loading and management of system prompts.

Features:
- YAML-based prompt templates
- Dynamic prompt loading
- Error handling for missing or malformed prompts

### 7. API Endpoints (`app/api`)

The API module provides FastAPI endpoints for external interaction.

Endpoints:
- **Health Check** (`/health`): Application status monitoring
- **Interaction** (`/interact`): Main endpoint for user-agent interaction

### 8. Data Schemas (`app/mcp_schemas`)

The Schemas module contains auto-generated Pydantic models for data validation.

Providers:
- **ITAPIA**: Complex financial analysis schemas
- **YF**: Yahoo Finance real-time price schemas

These models ensure type safety and data validation when interacting with external services.

## Data Flow

1. **Configuration Loading**: Application starts by loading environment variables
2. **LLM Initialization**: LLM client is created based on configuration
3. **Tool Discovery**: Tools are dynamically discovered from the MCP registry
4. **Agent Creation**: LangChain agent is configured with LLM, tools, and prompts
5. **API Startup**: FastAPI application is initialized with endpoints
6. **User Interaction**: 
   - User sends message via `/interact` endpoint
   - Agent retrieves session history
   - Agent processes message, potentially calling tools
   - Response is generated and history is updated
   - Response is returned to user

## Extensibility

The modular architecture allows for easy extension:

- **New LLM Providers**: Add new provider modules in `app/llms/`
- **New Tools**: Register tools in the MCP Servers registry
- **New Memory Backends**: Extend the factory pattern in `app/memory/`
- **New Prompts**: Add to the `prompts.yaml` file