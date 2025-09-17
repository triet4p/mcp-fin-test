# Tools Discovery Module

The Tools Discovery module handles the dynamic discovery and creation of tools that the financial agent can use. It connects to an MCP Servers registry to fetch tool specifications and creates LangChain tools from them.

## Components

### Tools Discovery (`tools_discovery.py`)

This module contains functions for:

1. **Dynamic Schema Import**: Importing Pydantic schema classes based on provider and class name
2. **Tool Creation**: Creating LangChain StructuredTools from specifications
3. **Tool Discovery**: Connecting to the MCP registry to fetch available tools

### Key Functions

#### `_get_schema_class(provider: str, class_name: str) -> Type[BaseModel]`

Dynamically imports a Pydantic class, ensuring the schema has been synced:

1. Constructs the module path based on provider
2. Reloads the module if it was previously imported
3. Imports the module and retrieves the specified class
4. Handles import errors gracefully

#### `create_api_calling_tool_from_spec(spec: dict)`

Automatically creates a LangChain Tool by reading the spec and importing schemas dynamically:

1. Parses the tool specification
2. Creates a Pydantic model for the tool's arguments
3. Defines an execution function that makes API calls
4. Returns a StructuredTool ready for use

#### `discover_tools()`

Discovers and builds a list of tools by calling the Registry Service:

1. Connects to the MCP Servers registry
2. Fetches tool specifications
3. Creates LangChain tools from specifications
4. Returns the list of tools

## Tool Specification Format

Tools are defined using a specification format that includes:

- `name`: The tool's name
- `description`: A description of what the tool does
- `endpoint`: The API endpoint template
- `method`: The HTTP method (GET, POST, etc.)
- `args_schema`: A schema defining the tool's arguments
- `provider`: The provider associated with the tool

## Usage Flow

```
Agent Initialization → discover_tools() → Registry Service → Tool Specifications → 
create_api_calling_tool_from_spec() → LangChain Tools → Agent Tools
```

This dynamic approach allows the agent to automatically discover and use new tools without code changes.