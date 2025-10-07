import json
import os
from typing import Dict, List, Any

class CommandDatabase:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.commands = {}
        self.category_mapping = {}
        self.command_mapping = {}
        self.favorites = set()
        self.load_data()
    
    def load_data(self):
        """加载所有数据"""
        try:
            # 加载指令数据库
            commands_path = os.path.join(self.data_dir, "commands.json")
            if os.path.exists(commands_path):
                with open(commands_path, 'r', encoding='utf-8') as f:
                    self.commands = json.load(f)
            
            # 加载分类映射
            category_mapping_path = os.path.join(self.data_dir, "category_mapping.json")
            if os.path.exists(category_mapping_path):
                with open(category_mapping_path, 'r', encoding='utf-8') as f:
                    self.category_mapping = json.load(f)
            
            # 加载指令映射
            command_mapping_path = os.path.join(self.data_dir, "command_mapping.json")
            if os.path.exists(command_mapping_path):
                with open(command_mapping_path, 'r', encoding='utf-8') as f:
                    self.command_mapping = json.load(f)
                    
        except Exception as e:
            print(f"加载数据失败: {e}")
    
    def get_categories(self) -> List[str]:
        """获取所有分类"""
        return list(self.commands.keys())
    
    def get_commands_by_category(self, category: str) -> Dict[str, Any]:
        """根据分类获取指令"""
        return self.commands.get(category, {})
    
    def get_command_info(self, category: str, command: str) -> Dict[str, Any]:
        """获取指令详细信息"""
        category_commands = self.get_commands_by_category(category)
        return category_commands.get(command, {})
    
    def get_category_display_name(self, category: str) -> str:
        """获取分类的显示名称"""
        return self.category_mapping.get(category, category)
    
    def get_command_display_name(self, command: str) -> str:
        """获取指令的显示名称"""
        return self.command_mapping.get("command_names", {}).get(command, command)
    
    def get_command_description(self, command: str) -> str:
        """获取指令的描述"""
        return self.command_mapping.get("command_descriptions", {}).get(command, "")
    
    def get_parameter_display_name(self, param_name: str) -> str:
        """获取参数的显示名称"""
        return self.command_mapping.get("parameter_names", {}).get(param_name, param_name)
    
    def get_parameter_description(self, param_name: str) -> str:
        """获取参数的描述"""
        return self.command_mapping.get("parameter_descriptions", {}).get(param_name, "")
    
    def get_parameter_placeholder(self, param_name: str) -> str:
        """获取参数的占位符"""
        return self.command_mapping.get("parameter_placeholders", {}).get(param_name, "")
    
    def get_option_display_name(self, option: str) -> str:
        """获取选项的显示名称"""
        return self.command_mapping.get("option_names", {}).get(option, option)
    
    def add_favorite(self, command_path: str):
        """添加到收藏"""
        self.favorites.add(command_path)
    
    def remove_favorite(self, command_path: str):
        """从收藏移除"""
        self.favorites.discard(command_path)
    
    def is_favorite(self, command_path: str) -> bool:
        """检查是否为收藏"""
        return command_path in self.favorites