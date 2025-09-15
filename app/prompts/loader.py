import yaml
from pathlib import Path

PROMPTS_DIR = Path(__file__).parent

def load_prompt(prompt_name: str, prompts_file: str = 'prompts.yaml') -> str:
    file_path = PROMPTS_DIR / prompts_file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Sử dụng safe_load để bảo mật hơn
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
        # Bắt các lỗi khác như YAML không hợp lệ
        raise RuntimeError(f"Could not load prompt '{prompt_name}' from {file_path}: {e}")