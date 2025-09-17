"""
Configuration module for the MCP Servers.

This module loads environment variables and sets up configuration constants
used throughout the MCP Servers application. It handles API routes and
configuration file paths.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API base route configuration
API_V1_BASE_ROUTE = os.getenv('API_V1_BASE_ROUTE', '/api/v1')

# Configuration file paths
TOOLS_FILE = os.getenv('TOOLS_FILE', 'spec/tools.yaml')
PROVIDERS_FILE = os.getenv("PROVIDERS_FILE", 'spec/providers.yaml')
