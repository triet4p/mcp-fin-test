from langchain_google_genai import ChatGoogleGenerativeAI
import app.core.config as cfg

def get_model():
    if not cfg.GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set for the Google provider.")
    return ChatGoogleGenerativeAI(
        model=cfg.CHAT_MODEL,
        google_api_key=cfg.GOOGLE_API_KEY,
        convert_system_message_to_human=True
    )