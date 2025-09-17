"""
Dependency management module for the MCP Servers.

This module handles the loading and caching of configuration data such as
tools and providers. It ensures that configuration files are only loaded once
and reused across the application.
"""
from typing import Any, Dict, List
import app.core.config as cfg
from app.core.loader import load_yaml_file

# Global variables to cache loaded configuration data
# This ensures we only load files once and reuse the data
_TOOLS: List[Dict[str, Any]] = None
_PROVIDERS: List[Dict[str, Any]] = None

def get_tools():
    """
    Get tool specifications from the configuration file.
    
    This function loads the tools configuration file if it hasn't been loaded yet,
    and returns the parsed tool specifications. The result is cached for future calls.
    
    Returns:
        List[Dict[str, Any]]: List of tool specifications
    """
    global _TOOLS
    if _TOOLS is None:
        _TOOLS = load_yaml_file(cfg.TOOLS_FILE)
    return _TOOLS

def get_providers():
    """
    Get provider configurations from the configuration file.
    
    This function loads the providers configuration file if it hasn't been loaded yet,
    and returns the parsed provider configurations. The result is cached for future calls.
    
    Returns:
        List[Dict[str, Any]]: List of provider configurations
    """
    global _PROVIDERS
    if _PROVIDERS is None:
        _PROVIDERS = load_yaml_file(cfg.PROVIDERS_FILE)
    return _PROVIDERS