from langchain_openai.chat_models import ChatOpenAI

import app.core.config as cfg

def get_model():
    if not cfg.OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY is not set for the OpenAI provider.")
    return ChatOpenAI(
        model=cfg.CHAT_MODEL,
        api_key=cfg.OPENROUTER_API_KEY,
        default_headers={
            'HTTP-Referer': cfg.API_V1_BASE_ROUTE,
            'X-Title': 'MCP Finance Test'
        },
        base_url=cfg.OPENROUTER_BASE_URL
    )