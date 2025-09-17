import requests
import sys
import importlib
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, create_model, Field
from typing import Dict, Any, Literal, Type
import app.core.config as cfg

def _get_schema_class(provider: str, class_name: str) -> Type[BaseModel]:
    """Import động một class Pydantic, đảm bảo schema đã được đồng bộ trước."""
    if not class_name or not provider: return None

    try:
        module_path = f"app.mcp_schemas.{provider}"
        # Xóa cache của module nếu nó đã được import trước đó để tải lại
        if module_path in sys.modules:
            importlib.reload(sys.modules[module_path])
        
        schema_module = importlib.import_module(module_path)
        return getattr(schema_module, class_name)
    except (ImportError, AttributeError, ModuleNotFoundError) as e:
        print(f"WARNING:  Không thể import động schema '{class_name}' từ module '{module_path}': {e}")
        return None

def create_api_calling_tool_from_spec(spec: dict):
    """Tự động tạo LangChain Tool bằng cách đọc spec và import động schema."""
    name = spec['name']
    tool_description = spec['description']
    endpoint_template = spec['endpoint']
    method = spec['method'].upper()
    provider = spec.get('provider')
    
    args_schema_dict = spec.get('args_schema', {})
    properties = args_schema_dict.get('properties', {})
    
    # --- THAY ĐỔI LOGIC TẠO MODEL BẮT ĐẦU TỪ ĐÂY ---
    
    required_params = args_schema_dict.get('required', [])
    fields_for_model = {}
    body_param_name = None

    for param_name, details in properties.items():
        is_required = param_name in required_params

        # Logic xử lý schema phức tạp
        if 'schemas_name' in details:
            body_param_name = param_name
            schema_class = _get_schema_class(provider, details['schemas_name'])
            
            # Tham số object phức tạp thường là bắt buộc
            field_value = Field(..., description=details.get('description'))
            fields_for_model[param_name] = (schema_class, field_value)
        
        # Logic xử lý schema đơn giản
        else: 
            # Xác định kiểu dữ liệu (logic này đã đúng)
            if 'enum' in details and isinstance(details['enum'], list):
                py_type = Literal[tuple(details['enum'])]
            else:
                py_type_str = details.get('type', 'string')
                py_type = {'string': str, 'integer': int, 'number': float, 'boolean': bool}.get(py_type_str, str)
            
            # --- LOGIC QUYẾT ĐỊNH GIÁ TRỊ CỦA FIELD ---
            description = details.get('description', '')
            
            if is_required:
                # Nếu bắt buộc, giá trị đầu tiên của Field là ... (Ellipsis)
                field_value = Field(..., description=description)
            else:
                # Nếu không bắt buộc, giá trị đầu tiên là giá trị mặc định
                # details.get('default') sẽ trả về None nếu không có default, Pydantic sẽ tự xử lý
                default_value = details.get('default')
                field_value = Field(default=default_value, description=description)

            fields_for_model[param_name] = (py_type, field_value)

    ArgsModel = create_model(f"{name.title().replace('_', '')}Input", **fields_for_model)

    def _execute_api_call(*args, **kwargs):
        try:
            # Hợp nhất args và kwargs lại thành một dict duy nhất
            # để xử lý một cách nhất quán.
            # Ví dụ, nếu tool chỉ có 1 arg là ticker, LangChain có thể gọi: _execute_api_call('FPT')
            # Đoạn code này sẽ chuyển nó thành {'ticker': 'FPT'}
            all_args = kwargs
            if args:
                # Lấy tên các field từ Pydantic model đã được tạo
                arg_names = list(ArgsModel.model_fields.keys())
                for i, arg_val in enumerate(args):
                    if i < len(arg_names):
                        all_args[arg_names[i]] = arg_val

            request_body = None
            if body_param_name and body_param_name in all_args:
                request_body = all_args.pop(body_param_name).model_dump()

            # Bây giờ, all_args chỉ chứa các tham số path và query
            formatted_endpoint = endpoint_template.format(**all_args)
            query_params = {k: v for k, v in all_args.items()}

            response = requests.request(
                method=method,
                url=formatted_endpoint,
                params=query_params,
                json=request_body,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"Lỗi khi gọi tool '{name}': {e}"}

    return StructuredTool.from_function(
        name=name,
        description=tool_description,
        func=_execute_api_call,
        args_schema=ArgsModel
    )

def discover_tools():
    """Khám phá và xây dựng danh sách tool bằng cách gọi đến Registry Service."""
    if not cfg.MCP_SERVERS_REGISTRY_URL:
        raise ValueError("MCP_SERVERS_REGISTRY_URL không được cấu hình.")
    try:
        print(f"INFO:     Đang khám phá tools từ Registry...")
        tools_response = requests.get(f"{cfg.MCP_SERVERS_REGISTRY_URL}/tools")
        tools_response.raise_for_status()
        tool_specs = tools_response.json()
        print(tool_specs)

        # 4. Tạo tool, truyền schema_manager vào
        tools = [create_api_calling_tool_from_spec(spec) for spec in tool_specs]
        for tool in tools:
            print(tool.description)
        print(f"INFO:     Đã khám phá và tạo thành công {len(tools)} tool.")
        return tools
    except Exception as e:
        print(f"ERROR:    Không thể khám phá tool từ Registry: {e}")
        return []