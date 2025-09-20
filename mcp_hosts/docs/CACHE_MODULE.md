# Cache Module

The Cache module implements caching mechanisms for the MCP Financial Agent to improve response times and reduce API costs by storing and reusing previous LLM responses.

## Supported Cache Types

1. **GPTCache** (`gptcache.py`): Semantic caching using vector similarity search
2. **Redis** (`redis.py`): Distributed caching using Redis
3. **In-Memory** (`in_memory.py`): Local caching in application memory

## Components

### Cache Factory (`_factory.py`)

The cache factory provides a factory pattern implementation for creating cache instances based on configuration:

1. **Cache Selection**: Reads the `LLM_CACHE_TYPE` environment variable to determine which cache type to use
2. **Instance Creation**: Initializes and returns the appropriate cache instance
3. **Error Handling**: Raises TypeError for unsupported cache types

### GPTCache Implementation (`gptcache.py`)

The GPTCache implementation provides semantic caching capabilities:

1. **Semantic Similarity**: Uses HuggingFace embeddings to convert prompts into vectors
2. **Vector Storage**: Stores cached responses in ChromaDB vector database
3. **Similarity Search**: Finds semantically similar prompts to retrieve cached responses
4. **Namespace Isolation**: Uses hashed LLM identifiers to isolate caches per model

### Redis Implementation (`redis.py`)

The Redis implementation provides distributed caching:

1. **Persistence**: Cached responses are stored in Redis for persistence across application restarts
2. **Sharing**: Multiple application instances can share the same cache
3. **Performance**: Fast retrieval of cached responses using Redis key-value store

### In-Memory Implementation (`in_memory.py`)

The in-memory implementation provides local caching:

1. **Speed**: Fastest cache access using local memory
2. **Simplicity**: Simple key-value storage for cached responses
3. **Development**: Ideal for development and testing environments

## Custom Agent Executor

The cache module is integrated with a custom agent executor (`SemanticMemoryAndCacheAgentExecutor`) that:

1. **Context-Aware Caching**: Creates cache keys that include both user question and relevant conversation history
2. **Cache Lookup**: Checks cache for existing responses before executing the agent
3. **Cache Update**: Stores new responses in cache after agent execution
4. **History Management**: Updates chat history with new interactions

The cache key is constructed by combining:
- Retrieved relevant conversation history from the Memory Retriever
- Current user question

This ensures that responses are cached in context, providing more accurate cached responses.

## Configuration

The cache module is configured through environment variables:

- `LLM_CACHE_ENABLED`: Enable/disable caching (true/false)
- `LLM_CACHE_TYPE`: Determines which cache backend to use (gptcache, redis, in-memory)
- `REDIS_HOST`: Redis server hostname (used by Redis cache)
- `REDIS_PORT`: Redis server port (used by Redis cache)
- `REDIS_DB`: Redis database number (used by Redis cache)
- `EMBEDDING_MODEL`: HuggingFace model for embeddings (used by GPTCache)

## Usage

The cache is automatically enabled based on configuration:

```python
# In agent factory
from app.cache import get_agent_cache
from langchain_core.globals import set_llm_cache

# Set the global LLM cache
set_llm_cache(get_agent_cache())
```

The custom agent executor handles cache operations:

```python
# Check cache
cached_result = self.agent_cache.lookup(cache_key, "")

# Update cache
self.agent_cache.update(cache_key, "", [Generation(text=dumps(result))])
```

This approach allows the application to reduce LLM API usage while maintaining contextual accuracy of responses.