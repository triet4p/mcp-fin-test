from typing import List, Dict, Any
import yaml

def load_yaml_file(file_path: str) -> List[Dict[str, Any]]:
    """Tải và phân tích cú pháp một file YAML một cách an toàn."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"ERROR: Configuration file not found at {file_path}")
        return [{}]
    except yaml.YAMLError as e:
        print(f"ERROR: Invalid YAML format in {file_path}: {e}")
        return [{}]