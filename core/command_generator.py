from typing import Dict, Any, List

class CommandGenerator:
    @staticmethod
    def generate_command(base_command: str, parameters: Dict[str, Any]) -> str:
        """生成完整的控制台指令"""
        # 如果指令不需要参数，直接返回基础指令
        if not parameters:
            return base_command
        
        # 过滤掉空值和None
        valid_params = {}
        for key, value in parameters.items():
            if value is not None and value != "":
                valid_params[key] = value
        
        if not valid_params:
            return base_command
        
        # 处理不同类型的参数
        param_parts = []
        
        for key, value in valid_params.items():
            if isinstance(value, bool):
                if value:
                    param_parts.append(str(key))
            elif isinstance(value, (int, float)):
                param_parts.append(str(value))
            elif isinstance(value, str):
                # 处理带空格的字符串参数
                if " " in value:
                    param_parts.append(f'"{value}"')
                else:
                    param_parts.append(value)
        
        if param_parts:
            return f"{base_command} {' '.join(param_parts)}"
        else:
            return base_command
    
    @staticmethod
    def validate_parameters(command_info: Dict[str, Any], parameters: Dict[str, Any]) -> List[str]:
        """验证参数并返回错误信息列表"""
        errors = []
        
        # 如果没有参数定义，直接返回无错误
        if "parameters" not in command_info or not command_info["parameters"]:
            return errors
        
        for param_name, param_config in command_info["parameters"].items():
            if param_config.get("required", False):
                value = parameters.get(param_name)
                if value is None or value == "":
                    # 使用参数原文作为错误信息
                    errors.append(f"参数 '{param_name}' 是必填的")
                    continue
                
                # 类型验证
                param_type = param_config.get("type", "string")
                if param_type == "int":
                    try:
                        int(value)
                    except ValueError:
                        errors.append(f"参数 '{param_name}' 必须是整数")
                elif param_type == "float":
                    try:
                        float(value)
                    except ValueError:
                        errors.append(f"参数 '{param_name}' 必须是数字")
        
        return errors