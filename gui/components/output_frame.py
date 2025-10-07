import customtkinter as ctk
import pyperclip
from tkinter import messagebox

class OutputFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """设置输出框架UI"""
        # 标题
        self.title_label = ctk.CTkLabel(self, text="生成的指令", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=(10, 5))
        
        # 操作按钮框架
        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.pack(fill="x", padx=10, pady=5)
        
        # 复制按钮
        self.copy_button = ctk.CTkButton(
            self.buttons_frame,
            text="复制到剪贴板",
            command=self.copy_to_clipboard,
            state="disabled"
        )
        self.copy_button.pack(side="left", padx=(0, 5))
        
        # 清除按钮
        self.clear_button = ctk.CTkButton(
            self.buttons_frame,
            text="清除",
            command=self.clear_output,
            fg_color="gray",
            hover_color="dark gray"
        )
        self.clear_button.pack(side="left")
        
        # 输出文本框
        self.output_text = ctk.CTkTextbox(
            self,
            wrap="word",
            font=("Consolas", 12)
        )
        self.output_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # 错误信息标签
        self.error_label = ctk.CTkLabel(
            self,
            text="",
            text_color="red",
            wraplength=300
        )
    
    def update_preview(self, command: str, error_message: str = ""):
        """更新指令预览"""
        if error_message:
            # 显示错误信息
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", command)
            self.output_text.configure(state="disabled")
            
            self.error_label.configure(text=error_message)
            self.error_label.pack(fill="x", padx=10, pady=5)
            
            self.copy_button.configure(state="disabled")
        else:
            # 显示生成的指令
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", command)
            self.output_text.configure(state="normal")
            
            self.error_label.pack_forget()
            self.copy_button.configure(state="normal")
    
    def copy_to_clipboard(self):
        """复制指令到剪贴板"""
        command = self.output_text.get("1.0", "end-1c")
        if command:
            pyperclip.copy(command)
            messagebox.showinfo("成功", "指令已复制到剪贴板！")
    
    def clear_output(self):
        """清除输出"""
        self.output_text.delete("1.0", "end")
        self.error_label.pack_forget()
        self.copy_button.configure(state="disabled")