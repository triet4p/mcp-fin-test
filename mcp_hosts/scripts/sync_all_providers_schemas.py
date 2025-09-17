# /scripts/sync_all_providers_schemas.py
import os
import requests
import subprocess
import sys
from pathlib import Path

# Lấy các cấu hình cần thiết. Trong Docker, bạn có thể truyền chúng qua biến môi trường.
REGISTRY_URL = os.getenv('MCP_SERVERS_REGISTRY_URL')
SYNC_SCRIPT_PATH = Path(__file__).parent / "sync_schemas.py"
OUTPUT_DIR = Path(__file__).parent.parent / "app" / "mcp_schemas"

def main():
    print(f"Bắt đầu đồng bộ schema từ Registry: {REGISTRY_URL}")
    try:
        # Lấy danh sách providers
        providers_response = requests.get(f"{REGISTRY_URL}/providers")
        providers_response.raise_for_status()
        providers = providers_response.json()
        
        print(f"Tìm thấy {len(providers)} provider: {[p['name'] for p in providers]}")

        # Đồng bộ cho mỗi provider
        for provider in providers:
            name = provider['name']
            base_url = provider['base_url']
            openapi_url = f"{base_url}/openapi.json"
            output_file = OUTPUT_DIR / f"{name}.py"
            
            print(f"--- Đang đồng bộ cho provider '{name}' ---")
            command = [
                "python", str(SYNC_SCRIPT_PATH),
                "--url", openapi_url,
                "--output", str(output_file)
            ]
            subprocess.run(command, check=True)
            
        print("✅ Đồng bộ tất cả schema thành công!")
        
    except Exception as e:
        print(f"❌ Lỗi trong quá trình đồng bộ: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()