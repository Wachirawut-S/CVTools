import nbformat
from tkinter import filedialog, messagebox

def generate_notebook(steps):
    nb = nbformat.v4.new_notebook()
    nb.cells = [nbformat.v4.new_code_cell(step["code"]) for step in steps]
    
    file_path = filedialog.asksaveasfilename(
        defaultextension=".ipynb",
        filetypes=[("IPython Notebook", "*.ipynb")],
        title="Save Notebook As"
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)
        messagebox.showinfo("Success", f"Notebook saved to {file_path}")
