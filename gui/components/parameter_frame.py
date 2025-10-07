import customtkinter as ctk
from typing import Dict, Any, Callable

class ParameterFrame(ctk.CTkFrame):
    def __init__(self, parent, parameter_changed_callback: Callable):
        super().__init__(parent)
        self.parameter_changed_callback = parameter_changed_callback
        self.current_command = None
        self.parameter_widgets = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置参数框架UI"""
        # 标题
        self.title_label = ctk.CTkLabel(self, text="指令参数", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=(10, 5))
        
        # 指令信息框架
        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.pack(fill="x", padx=10, pady=5)
        
        self.command_name_label = ctk.CTkLabel(
            self.info_frame, 
            text="请选择指令", 
            font=("Arial", 14, "bold")
        )
        self.command_name_label.pack(pady=5)
        
        # 指令原文标签（小字）
        self.command_original_label = ctk.CTkLabel(
            self.info_frame,
            text="",
            text_color="gray",
            font=("Arial", 10)
        )
        self.command_original_label.pack(pady=(0, 2))
        
        self.command_desc_label = ctk.CTkLabel(
            self.info_frame, 
            text="", 
            wraplength=400,
            text_color="gray",
            font=("Arial", 11)
        )
        self.command_desc_label.pack(pady=(0, 5))
        
        # 参数输入框架
        self.parameters_scrollable = ctk.CTkScrollableFrame(self)
        self.parameters_scrollable.pack(fill="both", expand=True, padx=10, pady=5)
        
        # 初始提示
        self.placeholder_label = ctk.CTkLabel(
            self.parameters_scrollable,
            text="选择左侧的指令开始配置参数",
            text_color="gray",
            font=("Arial", 12)
        )
        self.placeholder_label.pack(pady=50)
    
    def set_command_info(self, command: str, command_info: Dict[str, Any], db=None):
        """设置当前指令信息"""
        self.current_command = command
        self.command_info = command_info
        self.db = db  # 存储数据库引用用于获取映射
        
        # 获取指令的显示名称和描述
        if db:
            display_name = db.get_command_display_name(command)
            description = db.get_command_description(command)
        else:
            display_name = command
            description = command_info.get("description", "")
        
        # 更新指令信息显示
        self.command_name_label.configure(text=display_name)
        self.command_original_label.configure(text=f"指令原文: {command}")
        self.command_desc_label.configure(text=description)
        
        # 清除旧参数组件
        self.clear_parameters()
        
        # 隐藏提示
        self.placeholder_label.pack_forget()
        
        # 检查是否有参数
        parameters = command_info.get("parameters", {})
        
        if parameters:
            # 有参数：创建参数输入组件
            self.create_parameter_widgets(parameters)
        else:
            # 无参数：显示提示信息
            self.show_no_parameters_message()
        
        # 立即触发参数变化，生成指令预览
        self.on_parameter_changed()
    
    def show_no_parameters_message(self):
        """显示无参数提示"""
        no_params_frame = ctk.CTkFrame(self.parameters_scrollable)
        no_params_frame.pack(fill="x", pady=20)
        
        no_params_label = ctk.CTkLabel(
            no_params_frame,
            text="该指令无需额外参数",
            text_color="green",
            font=("Arial", 12, "bold")
        )
        no_params_label.pack(pady=10)
        
        hint_label = ctk.CTkLabel(
            no_params_frame,
            text="直接复制右侧生成的指令即可使用",
            text_color="gray"
        )
        hint_label.pack()
    
    def clear_parameters(self):
        """清除所有参数组件"""
        for widget in self.parameters_scrollable.winfo_children():
            widget.destroy()
        
        self.parameter_widgets.clear()
    
    def create_parameter_widgets(self, parameters: Dict[str, Any]):
        """创建参数输入组件"""
        for param_name, param_config in parameters.items():
            self.create_parameter_widget(param_name, param_config)
    
    def create_parameter_widget(self, param_name: str, param_config: Dict[str, Any]):
        """创建单个参数输入组件"""
        param_frame = ctk.CTkFrame(self.parameters_scrollable)
        param_frame.pack(fill="x", pady=5)
        
        # 获取参数的显示名称和描述
        if self.db:
            display_param_name = self.db.get_parameter_display_name(param_name)
            description = self.db.get_parameter_description(param_name)
        else:
            display_param_name = param_name
            description = param_config.get("description", "")
        
        # 参数标签和说明
        required = param_config.get("required", False)
        label_text = f"{display_param_name}{' *' if required else ''}"
        
        label = ctk.CTkLabel(
            param_frame, 
            text=label_text,
            font=("Arial", 12, "bold")
        )
        label.pack(anchor="w", padx=5)
        
        # 参数原文标签（小字）
        original_label = ctk.CTkLabel(
            param_frame,
            text=f"参数原文: {param_name}",
            text_color="gray",
            font=("Arial", 9)
        )
        original_label.pack(anchor="w", padx=5)
        
        # 参数描述
        if description:
            desc_label = ctk.CTkLabel(
                param_frame,
                text=description,
                text_color="gray",
                wraplength=400,
                font=("Arial", 10)
            )
            desc_label.pack(anchor="w", padx=5)
        
        # 根据类型创建输入组件
        param_type = param_config.get("type", "string")
        widget = self.create_input_widget(param_frame, param_name, param_config, param_type)
        
        if widget:
            self.parameter_widgets[param_name] = widget
    
    def create_input_widget(self, parent, param_name: str, param_config: Dict[str, Any], param_type: str):
        """根据类型创建输入组件"""
        default_value = param_config.get("default", "")
        options = param_config.get("options", [])
        
        if self.db:
            placeholder = self.db.get_parameter_placeholder(param_name)
        else:
            placeholder = param_config.get("placeholder", "")
        
        if param_type == "bool":
            var = ctk.BooleanVar(value=bool(default_value))
            widget = ctk.CTkCheckBox(
                parent,
                text="启用",
                variable=var,
                command=lambda: self.on_parameter_changed()
            )
            widget.pack(anchor="w", padx=5, pady=2)
            return var
        
        elif param_type == "choice" and options:
            # 转换选项显示名称
            display_options = []
            option_mapping = {}
            for option in options:
                if self.db:
                    display_option = self.db.get_option_display_name(option)
                else:
                    display_option = option
                display_options.append(display_option)
                option_mapping[display_option] = option
            
            # 设置默认显示值
            default_display = ""
            if default_value:
                default_display = self.db.get_option_display_name(default_value) if self.db else default_value
            elif display_options:
                default_display = display_options[0]
            
            var = ctk.StringVar(value=default_display)
            widget = ctk.CTkComboBox(
                parent,
                values=display_options,
                variable=var,
                command=lambda e: self.on_parameter_changed()
            )
            widget.pack(fill="x", padx=5, pady=2)
            
            # 存储选项映射和原始参数名
            widget.option_mapping = option_mapping
            widget.param_name = param_name
            return var
        
        elif param_type == "int":
            var = ctk.StringVar(value=str(default_value))
            widget = ctk.CTkEntry(
                parent,
                textvariable=var,
                placeholder_text=placeholder
            )
            widget.pack(fill="x", padx=5, pady=2)
            widget.bind("<KeyRelease>", lambda e: self.on_parameter_changed())
            return var
        
        else:  # string, float 等
            var = ctk.StringVar(value=default_value)
            widget = ctk.CTkEntry(
                parent,
                textvariable=var,
                placeholder_text=placeholder
            )
            widget.pack(fill="x", padx=5, pady=2)
            widget.bind("<KeyRelease>", lambda e: self.on_parameter_changed())
            return var
    
    def on_parameter_changed(self):
        """处理参数变化"""
        parameters = self.collect_parameters()
        if self.parameter_changed_callback:
            self.parameter_changed_callback(parameters)
    
    def collect_parameters(self) -> Dict[str, Any]:
        """收集所有参数值"""
        parameters = {}
        
        for param_name, widget in self.parameter_widgets.items():
            if isinstance(widget, (ctk.StringVar, ctk.BooleanVar)):
                value = widget.get()
                
                # 处理下拉框的选项映射
                if hasattr(widget, 'option_mapping'):
                    # 将显示值映射回原始值
                    value = widget.option_mapping.get(value, value)
                
                # 类型转换
                param_config = self.command_info["parameters"][param_name]
                param_type = param_config.get("type", "string")
                
                if param_type == "int" and value:
                    try:
                        value = int(value)
                    except ValueError:
                        value = value  # 保持原样，验证时会报错
                elif param_type == "float" and value:
                    try:
                        value = float(value)
                    except ValueError:
                        value = value
                elif param_type == "bool":
                    value = bool(value)
                
                parameters[param_name] = value
        
        return parameters