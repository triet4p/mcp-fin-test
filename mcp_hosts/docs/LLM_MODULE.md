# LLM Module

The LLM module provides a factory pattern implementation for creating language model clients based on configuration. It supports multiple LLM providers and handles caching configuration.

## Supported Providers

1. **Google** (`google.py`): Google Gemini models
2. **OpenAI** (`openai.py`): OpenAI GPT models
3. **OpenRouter** (`openrouter.py`): Models via OpenRouter API
4. **Ollama** (`ollama.py`): Local models via Ollama

## Components

### LLM Factory (`_factory.py`)

The LLM factory is responsible for:

1. **Provider Selection**: Reading the `LLM_PROVIDER` environment variable to determine which provider to use
2. **Client Creation**: Initializing and returning the appropriate client
3. **Caching Setup**: Configuring Redis caching for LLM responses if enabled

### Provider Modules

Each provider module contains a `get_model()` function that:

1. Validates required API keys
2. Creates and configures the specific LLM client
3. Returns the configured client

## Configuration

The LLM module is configured through environment variables:

- `LLM_PROVIDER`: Determines which provider to use (google, openai, openrouter, ollama)
- `GOOGLE_API_KEY`: API key for Google models
- `OPENAI_API_KEY`: API key for OpenAI models
- `OPENROUTER_API_KEY`: API key for OpenRouter
- `OLLAMA_BASE_URL`: Base URL for Ollama (defaults to http://localhost:11434)
- `CHAT_MODEL`: Specific model to use (defaults to gemini-2.5-flash for Google, gpt-4o-mini for OpenAI)
- `LLM_CACHE_ENABLED`: Enable/disable LLM response caching

## Caching

When enabled, LLM responses are cached in Redis to improve performance and reduce API costs. The cache is configured using:

- `REDIS_HOST`: Redis server hostname
- `REDIS_PORT`: Redis server port
- `REDIS_DB`: Redis database number

## Usage

The factory automatically creates and initializes the configured LLM client at module load time, making it available throughout the application as `llm_client`.