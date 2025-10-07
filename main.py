import customtkinter as ctk
from gui.main_window import MainWindow

def main():
    # 设置外观模式
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    # 创建主窗口
    root = ctk.CTk()
    root.title("HOI4 控制台指令生成器")
    root.geometry("1200x700")
    root.minsize(1000, 600)
    
    # 创建主应用
    app = MainWindow(root)
    
    # 启动主循环
    root.mainloop()

if __name__ == "__main__":
    main()