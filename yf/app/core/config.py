"""
Configuration module for the Yahoo Finance service.

This module loads environment variables and sets up configuration constants
used throughout the Yahoo Finance service application.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API base route configuration
API_V1_BASE_ROUTE = os.getenv('API_V1_BASE_ROUTE', '/api/v1')