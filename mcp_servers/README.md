# MCP Servers Module

The MCP Servers module provides tool specifications and provider configurations to agent hosts in the MCP Financial Agent ecosystem. It acts as a registry service that allows agents to dynamically discover available tools and their configurations.

## Overview

MCP Servers is a FastAPI application that serves two primary endpoints:
1. `/tools` - Provides tool specifications that define available capabilities
2. `/providers` - Provides provider configurations that define external service connections

## Components

### Core Configuration (`app/core`)

The core configuration module handles application settings through environment variables:

- `API_V1_BASE_ROUTE`: Base route for API endpoints (default: `/api/v1`)
- `TOOLS_FILE`: Path to the tools specification YAML file (default: `spec/tools.yaml`)
- `PROVIDERS_FILE`: Path to the providers configuration YAML file (default: `spec/providers.yaml`)

### YAML Loader (`app/core/loader.py`)

This module provides safe loading and parsing of YAML configuration files. It handles error cases such as missing files or invalid YAML format.

### Dependencies (`app/dependencies.py`)

The dependencies module manages the loading and caching of configuration data. It ensures that configuration files are only loaded once and reused across the application through a singleton pattern.

### API Endpoints (`app/api`)

The API module provides FastAPI endpoints for external interaction:

1. **Health Check** (`/health`): Application status monitoring
2. **Tools** (`/tools`): Provides tool specifications to agent hosts
3. **Providers** (`/providers`): Provides provider configurations to agent hosts

## Configuration Files

### Tools Specification (`spec/tools.yaml`)

The tools specification file defines all available tools with their:
- Name and description
- Provider association
- Endpoint URL and HTTP method
- Argument schema definition

Each tool specification includes detailed usage instructions and limitations to guide the agent in proper tool selection and usage.

### Providers Configuration (`spec/providers.yaml`)

The providers configuration file defines external service providers with their:
- Name
- Base URL

This allows the system to route tool calls to the appropriate external services.

## Data Flow

1. **Application Startup**: 
   - Load environment variables
   - Initialize FastAPI application
   - Set up API routes

2. **Agent Discovery**:
   - Agent host calls `/tools` endpoint to discover available capabilities
   - Agent host calls `/providers` endpoint to discover service configurations
   - Configuration files are loaded and cached for subsequent requests

3. **Tool Usage**:
   - Agent uses tool specifications to create dynamic tools
   - Tools make calls to external services based on provider configurations

## Extensibility

The modular architecture allows for easy extension:
- **New Tools**: Add tool specifications to `spec/tools.yaml`
- **New Providers**: Add provider configurations to `spec/providers.yaml`
- **New Endpoints**: Add new API modules in `app/api/`

## Documentation
- [PROVIDERS](docs/PROVIDERS_MODULE.md)
- [TOOLS](docs/TOOLS_MODULE.md)