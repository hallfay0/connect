import tkinter as tk
from tkinter import filedialog, messagebox
import os

def select_repo_path():
    folder_selected = filedialog.askdirectory()
    entry_repo_path.delete(0, tk.END)
    entry_repo_path.insert(0, folder_selected)

def select_output_path():
    file_selected = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown files", "*.md")])
    entry_output_path.delete(0, tk.END)
    entry_output_path.insert(0, file_selected)

def start_integration():
    repo_path = entry_repo_path.get()
    output_md_file = entry_output_path.get()
    extensions = entry_extensions.get().split(',')
    if not repo_path or not output_md_file:
        messagebox.showwarning("Warning", "Please select both the repository path and output file path.")
        return
    # 调用处理文件的函数
    try:
        write_contents_to_md(repo_path, output_md_file, extensions if extensions != [''] else None)
        messagebox.showinfo("Success", "Integration completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def write_contents_to_md(directory, output_file, extensions=None):
    with open(output_file, 'w', encoding='utf-8') as md_file:
        for root, _, files in os.walk(directory):
            for file in files:
                if extensions is None or os.path.splitext(file)[1] in extensions:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, directory)
                    md_file.write(f'## {relative_path}\n\n```text\n')
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            sanitized_content = content.replace('```', '\\`\\`\\`')
                            md_file.write(sanitized_content)
                    except Exception as e:
                        print(f"Error reading file {file_path}: {e}")
                        md_file.write(f'Error reading file: {e}')
                    md_file.write('\n```\n\n')

# GUI布局
root = tk.Tk()
root.title("GitHub Repository to Markdown")

tk.Label(root, text="Repository Path:").grid(row=0, column=0, sticky='e')
entry_repo_path = tk.Entry(root, width=50)
entry_repo_path.grid(row=0, column=1)
tk.Button(root, text="Browse...", command=select_repo_path).grid(row=0, column=2)

tk.Label(root, text="Output Markdown File:").grid(row=1, column=0, sticky='e')
entry_output_path = tk.Entry(root, width=50)
entry_output_path.grid(row=1, column=1)
tk.Button(root, text="Browse...", command=select_output_path).grid(row=1, column=2)

tk.Label(root, text="File Extensions (comma-separated, e.g., .py,.md):").grid(row=2, column=0, sticky='e')
entry_extensions = tk.Entry(root, width=50)
entry_extensions.grid(row=2, column=1)

tk.Button(root, text="Start Integration", command=start_integration).grid(row=3, column=1, pady=10)

root.mainloop()
