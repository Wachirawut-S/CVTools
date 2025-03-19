import tkinter as tk
from tkinter import messagebox
from notebook_generator import generate_notebook
from step_manager import get_steps

class CVToolsApp:
    def __init__(self, master):
        self.master = master
        master.title("CVTools - Image Processing Notebook Generator")
        self.steps = get_steps()  # initial steps list

        self.create_widgets()

    def create_widgets(self):
        # Left frame: list of steps
        self.frame_left = tk.Frame(self.master)
        self.frame_left.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        tk.Label(self.frame_left, text="List of Steps:").pack(anchor="w")
        self.listbox_steps = tk.Listbox(self.frame_left, width=80, height=15)
        self.listbox_steps.pack(padx=5, pady=5)
        self.update_listbox()

        # Right frame: action buttons
        self.frame_right = tk.Frame(self.master)
        self.frame_right.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        tk.Button(self.frame_right, text="Add Step", command=self.open_add_step_window, width=20).pack(padx=5, pady=5)
        tk.Button(self.frame_right, text="Generate Notebook", command=self.generate_notebook, width=20).pack(padx=5, pady=5)

    def update_listbox(self):
        self.listbox_steps.delete(0, tk.END)
        for idx, step in enumerate(self.steps):
            self.listbox_steps.insert(tk.END, f"{idx+1}. {step['desc']}")

    def open_add_step_window(self):
        # Open a window for adding a new step.
        # The AddStepWindow class is defined in ui_add_step.py.
        from ui_add_step import AddStepWindow
        AddStepWindow(self.master, self)

    def generate_notebook(self):
        # Generate the notebook using the current steps.
        generate_notebook(self.steps)

    def refresh_steps(self, new_steps):
        self.steps = new_steps
        self.update_listbox()
