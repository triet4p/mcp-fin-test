# Memory Management Module

The Memory Management module handles conversation history storage with support for multiple backends. It ensures that conversation context is maintained across interactions.

## Supported Backends

1. **In-Memory** (`in_memory.py`): Temporary storage in application memory (development/testing)
2. **Redis** (`_factory.py`): Persistent storage using Redis (production)

## Components

### Memory Factory (`_factory.py`)

The memory factory uses a factory pattern to create chat message history instances based on configuration:

1. **Backend Selection**: Reads the `MEMORY_TYPE` environment variable
2. **Instance Creation**: Creates the appropriate chat history instance
3. **Error Handling**: Raises TypeError for unsupported backends

### In-Memory Implementation (`in_memory.py`)

The in-memory implementation provides temporary storage for development and testing:

1. **Session Storage**: Maintains a dictionary of chat histories keyed by session ID
2. **Instance Management**: Creates new chat history instances as needed

## Configuration

The memory module is configured through environment variables:

- `MEMORY_TYPE`: Determines which backend to use (in-memory, redis)
- `REDIS_HOST`: Redis server hostname (defaults to localhost)
- `REDIS_PORT`: Redis server port (defaults to 6379)
- `REDIS_DB`: Redis database number (defaults to 0)

## Usage

The factory automatically creates the appropriate chat history instance based on configuration:

```python
chat_history = get_chat_message_history(session_id)
```

This approach allows switching between backends without changing application code.