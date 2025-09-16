from langchain_ollama.chat_models import ChatOllama
import app.core.config as cfg

def get_model():
    return ChatOllama(
        model=cfg.CHAT_MODEL,
        base_url=cfg.OLLAMA_BASE_URL,
    )