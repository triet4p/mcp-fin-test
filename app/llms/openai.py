from langchain_openai.chat_models import ChatOpenAI

import app.core.config as cfg

def get_model():
    if not cfg.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set for the OpenAI provider.")
    return ChatOpenAI(
        model=cfg.CHAT_MODEL,
        api_key=cfg.OPENAI_API_KEY
    )