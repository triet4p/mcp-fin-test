#!/bin/sh

echo "Entrypoint: Bắt đầu quá trình khởi động..."

# --- BƯỚC 1: ĐỒNG BỘ TẤT CẢ SCHEMA ---
# Tạo một script Python mới để làm việc này.
# Script này sẽ gọi Registry, lấy danh sách providers, và chạy sync_schemas.py cho mỗi provider.
echo "Entrypoint: Đang đồng bộ tất cả schema một lần duy nhất..."
python /mcp-hosts/scripts/sync_all_providers_schemas.py

if [ $? -ne 0 ]; then
    echo "Entrypoint: Không thể đồng bộ schema, container sẽ dừng lại." >&2
    exit 1
fi

echo "Entrypoint: Schemas đã sẵn sàng. Đang khởi động ứng dụng chính (Uvicorn)..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# --- BƯỚC 2: CHẠY ỨNG DỤNG ---
# Bây giờ Uvicorn có thể reload thoải mái mà không bị ghi đè file nữa.
exec "$@"