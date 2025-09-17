# Agent Module

The Agent module is the core of the MCP Financial Agent, responsible for orchestrating interactions between the user, language model, and available tools.

## Components

### Agent Factory (`_factory.py`)

The agent factory creates and configures the LangChain agent with all necessary components:

1. **Prompt Template**: Defines the conversation structure including system instructions, chat history, user input, and agent scratchpad
2. **Tools**: Dynamically discovered tools that the agent can use
3. **LLM Client**: The configured language model provider
4. **Agent Executor**: Manages the agent's execution loop

### Key Functions

#### `get_agent_response(session_id: str, user_message: str) -> dict`

Processes user messages through the financial agent and returns responses:

1. Retrieves or creates chat history for the session
2. Invokes the agent with the user's message and chat history
3. Updates chat history with the new interaction
4. Returns the agent's response

## Usage Flow

```
User Message → get_agent_response() → Agent Executor → LLM → Tools (if needed) → Response
```

The agent uses a ReAct (Reasoning + Action) approach, where it can decide to use tools to gather information before formulating a response.