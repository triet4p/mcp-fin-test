import argparse
import sys
import time
from pathlib import Path
import requests
from datamodel_code_generator import DataModelType, PythonVersion, generate, InputFileType

def parse_args():
    """Phân tích các tham số dòng lệnh."""
    parser = argparse.ArgumentParser(
        description="Tự động tạo Pydantic models từ đặc tả OpenAPI của một service."
    )
    parser.add_argument(
        "--url",
        required=True,
        help="URL đầy đủ của file openapi.json.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Đường dẫn đến file Python đầu ra cho các schema.",
    )
    parser.add_argument(
        "--wait-timeout",
        type=int,
        default=60,
        help="Thời gian tối đa (giây) để chờ API sẵn sàng.",
    )
    return parser.parse_args()

def get_api_content(url: str, timeout: int) -> str | None:
    """
    Chờ API sẵn sàng và lấy nội dung JSON của nó.
    Trả về nội dung nếu thành công, None nếu thất bại.
    """
    print(f"Đang chờ API tại '{url}' sẵn sàng (tối đa {timeout} giây)...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=2)
            response.raise_for_status()
            print("✅ API đã sẵn sàng!")
            # Trả về nội dung text của response
            return response.text
        except requests.RequestException:
            time.sleep(2)
    
    print(f"❌ Không thể kết nối tới API sau {timeout} giây.", file=sys.stderr)
    return None

def main():
    """Hàm thực thi chính của script."""
    args = parse_args()
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 1. Chờ và lấy nội dung API
    api_content = get_api_content(args.url, args.wait_timeout)
    if not api_content:
        sys.exit(1) # Thoát nếu không lấy được nội dung

    # 2. Tạo schema từ nội dung đã lấy được
    try:
        print(f"Đang tạo Pydantic models từ nội dung của '{args.url}'...")
        
        # --- THAY ĐỔI QUAN TRỌNG ---
        # Thay vì truyền URL, chúng ta truyền trực tiếp nội dung chuỗi (string)
        # và chỉ định rõ loại input là OpenAPI.
        generate(
            input_=api_content,
            input_file_type=InputFileType.OpenAPI,
            output=output_path,
            output_model_type=DataModelType.PydanticV2BaseModel,
            target_python_version=PythonVersion.PY_311,
            keep_model_order=True,
            use_field_description=True,
            field_constraints=True,
        )
        
        print(f"✅ Đã tạo thành công schema tại: '{output_path}'")
    except Exception as e:
        print(f"❌ Đã xảy ra lỗi khi tạo schema: {e}", file=sys.stderr)
        # In ra traceback để có thêm thông tin chi tiết
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()