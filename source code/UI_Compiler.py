import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import sys
import tempfile

class CodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("C Code Editor")
        self.current_file = tk.StringVar(value="")
        
        # Thiết lập giao diện
        self.setup_ui()
        
        # Biến để lưu trạng thái file
        self.text_modified = False
        self.code_text.bind('<<Modified>>', self.on_text_modified)

    def setup_ui(self):
        # Menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)
        
        # Frame chính
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Khu vực nhập code
        tk.Label(self.main_frame, text="C Code Editor").pack(anchor="w")
        self.code_text = tk.Text(self.main_frame, wrap="none", height=20, width=80)
        self.code_text.pack(fill="both", expand=True, pady=(0, 10))
        
        # Console (hiển thị mã assembly hoặc lỗi)
        tk.Label(self.main_frame, text="Assembly Output").pack(anchor="w")
        self.console_text = tk.Text(self.main_frame, wrap="word", height=10, width=80, state="disabled")
        self.console_text.pack(fill="both", expand=True)
        
        # Thanh nút
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(fill="x", pady=5)
        tk.Button(button_frame, text="Compile", command=self.run_code).pack(side="left", padx=5)
        tk.Button(button_frame, text="Clear Console", command=self.clear_console).pack(side="left", padx=5)
        
        # Thanh trạng thái
        self.status_label = tk.Label(self.main_frame, text="Ready", anchor="w")
        self.status_label.pack(fill="x")

    def on_text_modified(self, event):
        if self.code_text.edit_modified():
            self.text_modified = True
            self.update_title()
            self.code_text.edit_modified(False)

    def update_title(self):
        file_name = self.current_file.get() or "Untitled"
        modified = "*" if self.text_modified else ""
        self.root.title(f"C Code Editor - {file_name}{modified}")

    def new_file(self):
        if self.check_save():
            self.code_text.delete("1.0", tk.END)
            self.current_file.set("")
            self.text_modified = False
            self.update_title()
            self.status_label.config(text="New file created")

    def open_file(self):
        if self.check_save():
            file_path = filedialog.askopenfilename(
                title="Open C File",
                filetypes=[("C Files", "*.c"), ("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if file_path:
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        self.code_text.delete("1.0", tk.END)
                        self.code_text.insert(tk.END, file.read())
                        self.current_file.set(file_path)
                        self.text_modified = False
                        self.update_title()
                        self.status_label.config(text=f"Opened: {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to open file: {str(e)}")

    def save_file(self):
        if self.current_file.get():
            try:
                with open(self.current_file.get(), "w", encoding="utf-8") as file:
                    file.write(self.code_text.get("1.0", "end-1c"))
                self.text_modified = False
                self.update_title()
                self.status_label.config(text=f"Saved: {self.current_file.get()}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".c",
            filetypes=[("C Files", "*.c"), ("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.code_text.get("1.0", "end-1c"))
                self.current_file.set(file_path)
                self.text_modified = False
                self.update_title()
                self.status_label.config(text=f"Saved as: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    def check_save(self):
        if self.text_modified:
            response = messagebox.askyesnocancel(
                "Save Changes",
                "Do you want to save changes to the current file?"
            )
            if response is True:
                self.save_file()
                return True
            elif response is False:
                return True
            return False
        return True

    def run_code(self):
        # Xóa console trước khi chạy
        self.clear_console()
        
        # Lưu mã C vào file tạm thời
        temp_c_path = None
        temp_s_path = None
        temp_exe_path = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".c", delete=False) as temp_c:
                temp_c.write(self.code_text.get("1.0", "end-1c").encode("utf-8"))
                temp_c_path = temp_c.name
            
            temp_s_path = temp_c_path.replace(".c", ".s")
            temp_exe_path = temp_c_path.replace(".c", "")
            
            # Gọi compiler.py để sinh mã assembly
            try:
                result = subprocess.run(
                    [sys.executable, "compiler.py", temp_c_path, temp_s_path],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode != 0:
                    self.console_text.config(state="normal")
                    self.console_text.insert(tk.END, f"Compiler Error:\n{result.stderr}")
                    self.console_text.config(state="disabled")
                    self.status_label.config(text="Compiler error")
                    return
                
                # Hiển thị mã assembly
                with open(temp_s_path, "r", encoding="utf-8") as s_file:
                    self.console_text.config(state="normal")
                    self.console_text.insert(tk.END, f"Generated Assembly Code:\n{'='*50}\n{s_file.read()}\n{'='*50}\n")
                    self.console_text.config(state="disabled")
                
                # Biên dịch mã assembly thành chương trình thực thi
                try:
                    result = subprocess.run(
                        ["gcc", "-no-pie", temp_s_path, "-o", temp_exe_path, "-lc"],
                        capture_output=True, text=True, timeout=10
                    )
                    if result.returncode != 0:
                        self.console_text.config(state="normal")
                        self.console_text.insert(tk.END, f"GCC Error:\n{result.stderr}")
                        self.console_text.config(state="disabled")
                        self.status_label.config(text="GCC compilation error")
                        return
                    
                    # Kiểm tra file thực thi tồn tại
                    if not os.path.exists(temp_exe_path):
                        self.console_text.config(state="normal")
                        self.console_text.insert(tk.END, f"Error: Executable file {temp_exe_path} not found\n")
                        self.console_text.config(state="disabled")
                        self.status_label.config(text="Executable not found")
                        return
                    
                    # Đảm bảo file thực thi có quyền thực thi
                    subprocess.run(["chmod", "+x", temp_exe_path], check=True)
                    
                    # Chạy chương trình trong terminal, xóa file tạm sau khi hoàn thành
                    try:
                        # Sử dụng đường dẫn tuyệt đối và xóa file trong lệnh bash
                        abs_exe_path = os.path.abspath(temp_exe_path)
                        abs_c_path = os.path.abspath(temp_c_path)
                        abs_s_path = os.path.abspath(temp_s_path)
                        subprocess.Popen([
                            "gnome-terminal",
                            "--",
                            "bash",
                            "-c",
                            f"{abs_exe_path}; echo 'Program finished. Press Enter to close.'; rm -f {abs_c_path} {abs_s_path} {abs_exe_path}; read"
                        ])
                        self.status_label.config(text="Program running in terminal")
                    except Exception as e:
                        self.console_text.config(state="normal")
                        self.console_text.insert(tk.END, f"Terminal Error: {str(e)}")
                        self.console_text.config(state="disabled")
                        self.status_label.config(text="Terminal error")
                
                except Exception as e:
                    self.console_text.config(state="normal")
                    self.console_text.insert(tk.END, f"GCC Compilation Error: {str(e)}")
                    self.console_text.config(state="disabled")
                    self.status_label.config(text="GCC compilation error")
            
            except Exception as e:
                self.console_text.config(state="normal")
                self.console_text.insert(tk.END, f"Compiler Error: {str(e)}")
                self.console_text.config(state="disabled")
                self.status_label.config(text="Compiler error")
        
        except Exception as e:
            self.console_text.config(state="normal")
            self.console_text.insert(tk.END, f"Error creating temporary file: {str(e)}")
            self.console_text.config(state="disabled")
            self.status_label.config(text="Temporary file error")
        
        # Không xóa file trong finally, để lệnh bash xử lý

    def clear_console(self):
        self.console_text.config(state="normal")
        self.console_text.delete("1.0", tk.END)
        self.console_text.config(state="disabled")
        self.status_label.config(text="Console cleared")

    def exit_app(self):
        if self.check_save():
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeEditor(root)
    root.mainloop()