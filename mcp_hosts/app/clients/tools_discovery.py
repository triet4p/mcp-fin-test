"""
Tools discovery module for the MCP Financial Agent.

This module handles the dynamic discovery and creation of tools that the
financial agent can use. It connects to an MCP Servers registry to fetch
tool specifications and creates LangChain tools from them.
"""
import requests
import sys
import importlib
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, create_model, Field
from typing import Dict, Any, Literal, Type
import app.core.config as cfg

def _get_schema_class(provider: str, class_name: str) -> Type[BaseModel]:
    """
    Dynamically import a Pydantic class, ensuring the schema has been synced.
    
    Args:
        provider (str): The provider name (e.g., 'itapia', 'yf')
        class_name (str): The name of the Pydantic class to import
        
    Returns:
        Type[BaseModel]: The Pydantic class or None if import fails
    """
    if not class_name or not provider: 
        return None

    try:
        module_path = f"app.mcp_schemas.{provider}"
        # Clear module cache if it was previously imported to reload
        if module_path in sys.modules:
            importlib.reload(sys.modules[module_path])
        
        schema_module = importlib.import_module(module_path)
        return getattr(schema_module, class_name)
    except (ImportError, AttributeError, ModuleNotFoundError) as e:
        print(f"WARNING:  Cannot dynamically import schema '{class_name}' from module '{module_path}': {e}")
        return None

def create_api_calling_tool_from_spec(spec: dict):
    """
    Automatically create a LangChain Tool by reading the spec and importing schemas dynamically.
    
    This function takes a tool specification and creates a callable LangChain tool
    that can make API requests according to the specification.
    
    Args:
        spec (dict): Tool specification containing name, description, endpoint, method, etc.
        
    Returns:
        StructuredTool: A LangChain tool ready to be used by the agent
    """
    name = spec['name']
    tool_description = spec['description']
    endpoint_template = spec['endpoint']
    method = spec['method'].upper()
    provider = spec.get('provider')
    
    args_schema_dict = spec.get('args_schema', {})
    properties = args_schema_dict.get('properties', {})
    
    required_params = args_schema_dict.get('required', [])
    fields_for_model = {}
    body_param_name = None

    for param_name, details in properties.items():
        is_required = param_name in required_params

        # Handle complex schema objects
        if 'schemas_name' in details:
            body_param_name = param_name
            schema_class = _get_schema_class(provider, details['schemas_name'])
            
            # Complex object parameters are typically required
            field_value = Field(..., description=details.get('description'))
            fields_for_model[param_name] = (schema_class, field_value)
        
        # Handle simple schema types
        else: 
            # Determine data type
            if 'enum' in details and isinstance(details['enum'], list):
                py_type = Literal[tuple(details['enum'])]
            else:
                py_type_str = details.get('type', 'string')
                py_type = {'string': str, 'integer': int, 'number': float, 'boolean': bool}.get(py_type_str, str)
            
            description = details.get('description', '')
            
            if is_required:
                # For required fields, the first value of Field is ... (Ellipsis)
                field_value = Field(..., description=description)
            else:
                # For optional fields, the first value is the default value
                default_value = details.get('default')
                field_value = Field(default=default_value, description=description)

            fields_for_model[param_name] = (py_type, field_value)

    ArgsModel = create_model(f"{name.title().replace('_', '')}Input", **fields_for_model)

    def _execute_api_call(*args, **kwargs):
        """
        Execute the API call for this tool.
        
        This function handles parameter processing, API request execution,
        and error handling for the tool.
        """
        try:
            # Merge args and kwargs into a single dict for consistent processing
            # For example, if the tool only has 1 arg 'ticker', LangChain might call: 
            # _execute_api_call('FPT') which this code converts to {'ticker': 'FPT'}
            all_args = kwargs
            if args:
                # Get field names from the created Pydantic model
                arg_names = list(ArgsModel.model_fields.keys())
                for i, arg_val in enumerate(args):
                    if i < len(arg_names):
                        all_args[arg_names[i]] = arg_val

            request_body = None
            if body_param_name and body_param_name in all_args:
                request_body = all_args.pop(body_param_name).model_dump()

            # Now all_args only contains path and query parameters
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
            return {"error": f"Error calling tool '{name}': {e}"}

    return StructuredTool.from_function(
        name=name,
        description=tool_description,
        func=_execute_api_call,
        args_schema=ArgsModel
    )

def discover_tools():
    """
    Discover and build a list of tools by calling the Registry Service.
    
    This function connects to the MCP Servers registry to fetch tool specifications
    and creates LangChain tools from them.
    
    Returns:
        list: List of StructuredTool objects
        
    Raises:
        ValueError: If MCP_SERVERS_REGISTRY_URL is not configured
    """
    if not cfg.MCP_SERVERS_REGISTRY_URL:
        raise ValueError("MCP_SERVERS_REGISTRY_URL is not configured.")
    try:
        print(f"INFO:     Discovering tools from Registry...")
        tools_response = requests.get(f"{cfg.MCP_SERVERS_REGISTRY_URL}/tools")
        tools_response.raise_for_status()
        tool_specs = tools_response.json()
        print(tool_specs)

        # Create tools from specifications
        tools = [create_api_calling_tool_from_spec(spec) for spec in tool_specs]
        for tool in tools:
            print(tool.description)
        print(f"INFO:     Successfully discovered and created {len(tools)} tools.")
        return tools
    except Exception as e:
        print(f"ERROR:    Cannot discover tools from Registry: {e}")
        return []