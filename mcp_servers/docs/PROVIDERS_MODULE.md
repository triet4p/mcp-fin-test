# Providers Module

The Providers module in MCP Servers provides the endpoint that delivers provider configurations to agent hosts. These configurations enable agents to properly route tool calls to external services.

## Components

### Providers API Endpoint (`app/api/providers.py`)

This module defines the endpoint for providing provider configurations:

#### `get_providers()` Endpoint

The endpoint that agent hosts call to discover available providers:

1. **Purpose**: Provide a list of all available provider configurations
2. **Method**: GET
3. **Path**: `/providers`
4. **Response**: List of provider configuration dictionaries

The endpoint uses a caching mechanism to load provider configurations only once and reuse them for subsequent requests.

### Provider Configurations (`spec/providers.yaml`)

Provider configurations define the external service providers with their connection details:

1. **Name**: Unique identifier for the provider
2. **Base URL**: Root URL for the provider's services

## Usage Flow

```
Agent Host Initialization → Call /providers Endpoint → Load Providers from YAML → 
Return Provider Configurations → Agent Routes Tool Calls Properly
```

## Configuration Format

Provider configurations follow a simple format:

```yaml
- name: provider_name
  base_url: http://service-url:port
```

## Caching

Provider configurations are cached in memory after first load to improve performance and reduce file I/O for subsequent requests. This is managed through the dependencies module.