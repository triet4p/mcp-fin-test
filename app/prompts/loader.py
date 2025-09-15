import yaml
from pathlib import Path

PROMPTS_DIR = Path(__file__).parent

def load_prompt(prompt_name: str, prompts_file: str = 'prompts.yaml') -> str:
    """
    Load a prompt template from a YAML file.
    
    This function reads prompt templates from a YAML file and returns the
    specified prompt. It uses safe_load for security and includes error
    handling for missing files or prompts.
    
    Args:
        prompt_name (str): The name/ID of the prompt to load
        prompts_file (str): The name of the YAML file containing prompts
        
    Returns:
        str: The prompt template string
        
    Raises:
        FileNotFoundError: If the prompts file doesn't exist
        ValueError: If the requested prompt is not found or is malformed
        RuntimeError: If there's an error parsing the YAML file
    """
    file_path = PROMPTS_DIR / prompts_file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Using safe_load for better security
            all_prompts = yaml.safe_load(f)
        
        if prompt_name not in all_prompts:
            raise ValueError(f"Prompt '{prompt_name}' not found in {file_path}")
        
        prompt_data = all_prompts[prompt_name]
        
        if 'template' not in prompt_data:
            raise ValueError(f"Prompt '{prompt_name}' in {file_path} is missing the 'template' key.")
            
        return prompt_data['template']

    except FileNotFoundError:
        raise FileNotFoundError(f"Prompts file not found at: {file_path}")
    except Exception as e:
        # Catch other exceptions like invalid YAML syntax
        raise RuntimeError(f"Could not load prompt '{prompt_name}' from {file_path}: {e}")