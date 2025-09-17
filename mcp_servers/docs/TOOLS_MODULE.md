# Tools Module

The Tools module in MCP Servers provides the endpoint that delivers tool specifications to agent hosts. These specifications enable agents to dynamically discover and utilize available capabilities.

## Components

### Tools API Endpoint (`app/api/tools.py`)

This module defines the main endpoint for providing tool specifications:

#### `get_tools()` Endpoint

The primary endpoint that agent hosts call to discover available tools:

1. **Purpose**: Provide a list of all available tool specifications
2. **Method**: GET
3. **Path**: `/tools`
4. **Response**: List of tool specification dictionaries

The endpoint uses a caching mechanism to load tool specifications only once and reuse them for subsequent requests.

### Tool Specifications (`spec/tools.yaml`)

Tool specifications define the available capabilities with detailed information:

1. **Name**: Unique identifier for the tool
2. **Provider**: Associated external service provider
3. **Description**: Detailed explanation of when and how to use the tool
4. **Endpoint**: URL template for the tool's API
5. **Method**: HTTP method for the tool's API
6. **Args Schema**: Definition of required and optional arguments

Each tool specification includes:
- Usage guidelines
- Limitations and constraints
- Example scenarios

## Usage Flow

```
Agent Host Initialization → Call /tools Endpoint → Load Tools from YAML → 
Return Tool Specifications → Agent Creates Dynamic Tools
```

## Specification Format

Tool specifications follow a standardized format that includes all necessary information for agents to properly use the tools:

```yaml
- name: tool_name
  provider: provider_name
  description: |
    Detailed description of the tool including when to use it and its limitations
  endpoint: http://service-url/path/{parameter}
  method: GET|POST|PUT|DELETE
  args_schema:
    type: object
    properties:
      parameter:
        type: string|integer|number|boolean
        description: Parameter description
        schemas_name: If occured, this will help dynamic tool discorvery exact schemas of a parameter.
    required:
      - parameter
```

## Caching

Tool specifications are cached in memory after first load to improve performance and reduce file I/O for subsequent requests. This is managed through the dependencies module.