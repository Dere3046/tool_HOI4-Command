import customtkinter as ctk
from typing import Callable, Dict, Any, List

class CategoryFrame(ctk.CTkFrame):
    def __init__(self, parent, db, command_selected_callback: Callable):
        super().__init__(parent)
        self.db = db
        self.command_selected_callback = command_selected_callback
        self.category_widgets = {}
        
        self.setup_ui()
        self.load_categories()
    
    def setup_ui(self):
        """设置分类框架UI"""
        # 标题
        self.title_label = ctk.CTkLabel(self, text="指令分类", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=(10, 5))
        
        # 搜索框
        self.search_entry = ctk.CTkEntry(self, placeholder_text="搜索指令名称、原文或描述...")
        self.search_entry.pack(fill="x", padx=10, pady=5)
        self.search_entry.bind("<KeyRelease>", self.on_search)
        
        # 分类列表框架
        self.categories_frame = ctk.CTkScrollableFrame(self)
        self.categories_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def load_categories(self):
        """加载分类数据"""
        categories = self.db.get_categories()
        
        for category in categories:
            # 创建分类组
            category_group = CategoryGroup(
                self.categories_frame, 
                category,
                self.db,
                self.on_command_clicked
            )
            category_group.pack(fill="x", pady=2)
            self.category_widgets[category] = category_group
    
    def on_command_clicked(self, category: str, command: str):
        """处理指令点击事件"""
        command_info = self.db.get_command_info(category, command)
        if self.command_selected_callback:
            self.command_selected_callback(category, command, command_info)
    
    def on_search(self, event):
        """处理搜索事件 - 增强搜索功能"""
        search_term = self.search_entry.get().lower().strip()
        
        for category, widget in self.category_widgets.items():
            widget.filter_commands(search_term)

class CategoryGroup(ctk.CTkFrame):
    def __init__(self, parent, category: str, db, command_callback: Callable):
        super().__init__(parent, corner_radius=5)
        self.category = category
        self.db = db
        self.command_callback = command_callback
        self.all_commands = {}
        self.command_widgets = {}  # 存储指令组件
        
        self.setup_ui()
        self.load_commands()
    
    def setup_ui(self):
        """设置分类组UI"""
        # 分类标题（可折叠）
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=5, pady=2)
        
        # 获取分类的显示名称
        display_category = self.db.get_category_display_name(self.category)
        
        self.toggle_button = ctk.CTkButton(
            self.header_frame,
            text=f"▶ {display_category}",
            width=20,
            height=20,
            corner_radius=10,
            command=self.toggle_commands
        )
        self.toggle_button.pack(side="left")
        
        # 命令容器（初始隐藏）
        self.commands_container = ctk.CTkFrame(self)
        self.is_expanded = False
    
    def update_display_name(self):
        """更新分类显示名称"""
        display_category = self.db.get_category_display_name(self.category)
        current_text = self.toggle_button.cget("text")
        
        # 保留展开/收起状态图标，只更新分类名称
        if current_text.startswith("▶"):
            new_text = f"▶ {display_category}"
        else:
            new_text = f"▼ {display_category}"
        
        self.toggle_button.configure(text=new_text)
        
        # 更新所有指令按钮的显示文本
        for command_name, widget_info in self.command_widgets.items():
            self.update_command_widget_display(command_name, widget_info)
    
    def update_command_widget_display(self, command_name: str, widget_info: dict):
        """更新指令组件的显示"""
        display_name = self.db.get_command_display_name(command_name)
        description = self.db.get_command_description(command_name)
        
        # 更新按钮文本
        widget_info['button'].configure(text=display_name)
        
        # 更新描述标签
        widget_info['description_label'].configure(text=description)
        
        # 更新原文标签
        original_text = f"指令原文: {command_name}"
        widget_info['original_label'].configure(text=original_text)
    
    def load_commands(self):
        """加载分类下的指令"""
        commands = self.db.get_commands_by_category(self.category)
        self.all_commands = commands
        self.command_widgets = {}
        
        for command_name, command_info in commands.items():
            # 创建指令组件
            command_widget = self.create_command_widget(command_name, command_info)
            self.command_widgets[command_name] = command_widget
    
    def create_command_widget(self, command_name: str, command_info: dict):
        """创建单个指令的完整组件"""
        # 指令容器
        command_container = ctk.CTkFrame(self.commands_container)
        command_container.pack(fill="x", padx=10, pady=1)
        
        # 获取显示信息
        display_name = self.db.get_command_display_name(command_name)
        description = self.db.get_command_description(command_name)
        original_text = f"指令原文: {command_name}"
        
        # 指令按钮
        btn = ctk.CTkButton(
            command_container,
            text=display_name,
            anchor="w",
            command=lambda cmd=command_name: self.command_callback(
                self.category, cmd
            ),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30")
        )
        btn.pack(fill="x", pady=(5, 0))
        
        # 指令描述（小字）
        desc_label = ctk.CTkLabel(
            command_container,
            text=description,
            text_color="gray",
            font=("Arial", 10),
            wraplength=300,
            justify="left"
        )
        desc_label.pack(fill="x", padx=5, pady=(0, 2))
        
        # 指令原文（小字）
        original_label = ctk.CTkLabel(
            command_container,
            text=original_text,
            text_color="gray",
            font=("Arial", 9),
            wraplength=300,
            justify="left"
        )
        original_label.pack(fill="x", padx=5, pady=(0, 5))
        
        return {
            'container': command_container,
            'button': btn,
            'description_label': desc_label,
            'original_label': original_label,
            'display_name': display_name,
            'description': description,
            'original_name': command_name
        }
    
    def toggle_commands(self):
        """切换指令显示"""
        display_category = self.db.get_category_display_name(self.category)
        
        if self.is_expanded:
            self.commands_container.pack_forget()
            self.toggle_button.configure(text=f"▶ {display_category}")
        else:
            self.commands_container.pack(fill="x", pady=(5, 0))
            self.toggle_button.configure(text=f"▼ {display_category}")
        
        self.is_expanded = not self.is_expanded
    
    def filter_commands(self, search_term: str):
        """根据搜索词过滤指令 - 增强搜索功能"""
        if not search_term:
            # 显示所有指令
            for widget_info in self.command_widgets.values():
                widget_info['container'].pack(fill="x", padx=10, pady=1)
            return
        
        # 过滤指令 - 同时搜索显示名称、原始名称和描述
        for command_name, widget_info in self.command_widgets.items():
            display_name_lower = widget_info['display_name'].lower()
            original_name_lower = widget_info['original_name'].lower()
            description_lower = widget_info['description'].lower()
            
            # 检查是否匹配显示名称、原始名称或描述
            if (search_term in display_name_lower or 
                search_term in original_name_lower or 
                search_term in description_lower):
                widget_info['container'].pack(fill="x", padx=10, pady=1)
            else:
                widget_info['container'].pack_forget()