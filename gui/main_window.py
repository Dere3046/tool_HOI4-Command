import customtkinter as ctk
from gui.components.category_frame import CategoryFrame
from gui.components.parameter_frame import ParameterFrame
from gui.components.output_frame import OutputFrame
from core.command_database import CommandDatabase
from core.command_generator import CommandGenerator

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.db = CommandDatabase()
        self.generator = CommandGenerator()
        
        self.current_category = None
        self.current_command = None
        self.current_parameters = {}
        
        self.setup_ui()
        self.setup_bindings()
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建主框架
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 三栏布局
        self.main_frame.grid_columnconfigure(0, weight=1)  # 分类栏
        self.main_frame.grid_columnconfigure(1, weight=2)  # 参数栏
        self.main_frame.grid_columnconfigure(2, weight=1)  # 输出栏
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # 分类选择框架
        self.category_frame = CategoryFrame(
            self.main_frame, 
            self.db,
            command_selected_callback=self.on_command_selected
        )
        self.category_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=5)
        
        # 指令参数框架
        self.parameter_frame = ParameterFrame(
            self.main_frame,
            parameter_changed_callback=self.on_parameters_changed
        )
        self.parameter_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # 输出框架
        self.output_frame = OutputFrame(self.main_frame)
        self.output_frame.grid(row=0, column=2, sticky="nsew", padx=(5, 0), pady=5)
    
    def setup_bindings(self):
        """设置事件绑定"""
        pass
    
    def on_command_selected(self, category: str, command: str, command_info: dict):
        """处理指令选择事件"""
        self.current_category = category
        self.current_command = command
        self.current_parameters = {}  # 重置参数
        
        # 更新参数框架，传递数据库引用
        self.parameter_frame.set_command_info(command, command_info, self.db)
    
    def on_parameters_changed(self, parameters: dict):
        """处理参数变化事件"""
        self.current_parameters = parameters
        self.generate_command_preview()
    
    def generate_command_preview(self):
        """生成指令预览"""
        if not self.current_command:
            return
        
        # 验证参数
        command_info = self.db.get_command_info(self.current_category, self.current_command)
        errors = self.generator.validate_parameters(command_info, self.current_parameters)
        
        if errors:
            error_text = "参数错误:\n" + "\n".join(f"• {error}" for error in errors)
            self.output_frame.update_preview("", error_text)
            return
        
        # 生成指令
        generated_command = self.generator.generate_command(
            self.current_command, 
            self.current_parameters
        )
        
        self.output_frame.update_preview(generated_command)