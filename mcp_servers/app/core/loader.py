"""
YAML loader module for the MCP Servers.

This module provides functionality to safely load and parse YAML configuration files.
It handles error cases such as missing files or invalid YAML format.
"""
from typing import List, Dict, Any
import yaml

def load_yaml_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Safely load and parse a YAML file.
    
    This function attempts to load a YAML file and returns its contents as a list of dictionaries.
    It handles common error cases such as missing files or invalid YAML format.
    
    Args:
        file_path (str): Path to the YAML file to load
        
    Returns:
        List[Dict[str, Any]]: Parsed YAML content as a list of dictionaries, 
                             or a list containing an empty dictionary if an error occurs
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"ERROR: Configuration file not found at {file_path}")
        return [{}]
    except yaml.YAMLError as e:
        print(f"ERROR: Invalid YAML format in {file_path}: {e}")
        return [{}]