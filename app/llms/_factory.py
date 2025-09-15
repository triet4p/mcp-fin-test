from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
import app.core.config as cfg

def get_llm_client() -> BaseChatModel:
    if cfg.LLM_PROVIDER == "google":
        if not cfg.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is not set for the Google provider.")
        return ChatGoogleGenerativeAI(
            model=cfg.CHAT_MODEL,
            google_api_key=cfg.GOOGLE_API_KEY,
            convert_system_message_to_human=True
        )
    elif cfg.LLM_PROVIDER == "openai":
        if not cfg.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set for the OpenAI provider.")
        return ChatOpenAI(
            model=cfg.CHAT_MODEL,
            api_key=cfg.OPENAI_API_KEY
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {cfg.LLM_PROVIDER}")
    
llm_client = get_llm_client()