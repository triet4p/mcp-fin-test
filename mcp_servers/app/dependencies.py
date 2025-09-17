from typing import Any, Dict, List
import app.core.config as cfg
from app.core.loader import load_yaml_file

_TOOLS: List[Dict[str, Any]] = None
_PROVIDERS: List[Dict[str, Any]] = None

def get_tools():
    global _TOOLS
    if _TOOLS is None:
        _TOOLS = load_yaml_file(cfg.TOOLS_FILE)
    return _TOOLS

def get_providers():
    global _PROVIDERS
    if _PROVIDERS is None:
        _PROVIDERS = load_yaml_file(cfg.PROVIDERS_FILE)
    return _PROVIDERS