import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from step_manager import get_steps, update_step

class EditStepWindow:
    def __init__(self, master, app, idx):
        self.master = master
        self.app = app
        self.idx = idx
        self.step = get_steps()[idx]
        self.top = tk.Toplevel(master)
        self.top.title(f"Edit Step - {self.step.get('desc')}")
        self.create_widgets()
    
    def create_widgets(self):
        if self.step.get("type") == "Import Image":
            tk.Label(self.top, text="Variable Name:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
            self.var_entry = tk.Entry(self.top)
            self.var_entry.insert(0, self.step.get("variable"))
            self.var_entry.grid(row=0, column=1, padx=5, pady=5)
            
            tk.Label(self.top, text="File Path:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
            self.file_entry = tk.Entry(self.top, width=50)
            self.file_entry.insert(0, self.step.get("file_path"))
            self.file_entry.grid(row=1, column=1, padx=5, pady=5)
            
            tk.Button(self.top, text="Update Step", command=self.save_import_edit).grid(row=2, column=0, columnspan=2, pady=10)
        elif self.step.get("type") == "Extract Color":
            tk.Label(self.top, text="Source Image Variable:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
            imported = [s.get("variable") for s in get_steps() if s.get("type") == "Import Image"]
            self.src_var = tk.StringVar(value=self.step.get("source"))
            self.src_dropdown = ttk.Combobox(self.top, textvariable=self.src_var, values=imported, state="readonly")
            self.src_dropdown.grid(row=0, column=1, padx=5, pady=5)
            
            tk.Label(self.top, text="New Variable Name:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
            self.new_var_entry = tk.Entry(self.top)
            self.new_var_entry.insert(0, self.step.get("variable"))
            self.new_var_entry.grid(row=1, column=1, padx=5, pady=5)
            
            tk.Label(self.top, text="Select Color:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
            self.color_var = tk.StringVar(value=self.step.get("color"))
            self.color_dropdown = ttk.Combobox(self.top, textvariable=self.color_var, values=["red", "green", "blue", "yellow", "cyan", "magenta", "pink"], state="readonly")
            self.color_dropdown.grid(row=2, column=1, padx=5, pady=5)
            
            tk.Button(self.top, text="Update Step", command=self.save_extract_edit).grid(row=3, column=0, columnspan=2, pady=10)
            
        elif self.step.get("type") == "Merge Image":
            tk.Label(self.top, text="Source Image Variable 1:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
            imported = [s.get("variable") for s in get_steps() if s.get("type") == "Import Image"]
            self.src1_var = tk.StringVar(value=self.step.get("source1"))
            self.src1_dropdown = ttk.Combobox(self.top, textvariable=self.src1_var, values=imported, state="readonly")
            self.src1_dropdown.grid(row=0, column=1, padx=5, pady=5)
            
            tk.Label(self.top, text="Source Image Variable 2:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
            self.src2_var = tk.StringVar(value=self.step.get("source2"))
            self.src2_dropdown = ttk.Combobox(self.top, textvariable=self.src2_var, values=imported, state="readonly")
            self.src2_dropdown.grid(row=1, column=1, padx=5, pady=5)
            
            tk.Label(self.top, text="New Variable Name:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
            self.merge_var_entry = tk.Entry(self.top)
            self.merge_var_entry.insert(0, self.step.get("variable"))
            self.merge_var_entry.grid(row=2, column=1, padx=5, pady=5)
            
            
            tk.Button(self.top, text="Update Step", command=self.save_merge_edit).grid(row=4, column=0, columnspan=2, pady=10)
            
    def save_import_edit(self):
        var_name = self.var_entry.get().strip()
        file_path = self.file_entry.get().strip()
        if not var_name or not file_path:
            messagebox.showerror("Error", "Both variable name and file path are required.")
            return
        new_code = f'''# Import Image for variable '{var_name}'
file_path = r"{file_path}"
{var_name} = cv2.imread(file_path)
{var_name}_rgb = cv2.cvtColor({var_name}, cv2.COLOR_BGR2RGB)
{var_name}_gray = cv2.cvtColor({var_name}, cv2.COLOR_BGR2GRAY)

plt.figure(figsize=(15,5))
plt.subplot(1,3,1)
plt.title("Original - {var_name}")
plt.imshow(cv2.cvtColor({var_name}, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(1,3,2)
plt.title("RGB - {var_name}")
plt.imshow({var_name}_rgb)
plt.axis('off')

plt.subplot(1,3,3)
plt.title("Gray - {var_name}")
plt.imshow({var_name}_gray, cmap='gray')
plt.axis('off')

plt.show()
'''
        new_step = self.step.copy()
        new_step["code"] = new_code
        new_step["variable"] = var_name
        new_step["file_path"] = file_path
        new_step["desc"] = f"Import Image (var: {var_name}, file: {file_path})"
        update_step(self.idx, new_step)
        self.app.refresh_steps(get_steps())
        messagebox.showinfo("Updated", "Import Image step updated successfully!")
        self.top.destroy()
    
    def save_extract_edit(self):
        source = self.src_var.get().strip()
        new_var = self.new_var_entry.get().strip()
        selected_color = self.color_var.get().strip()
        if not new_var:
            messagebox.showerror("Error", "New variable name cannot be empty.")
            return
        if selected_color.lower() == "red":
            lower = "[0, 120, 70]"
            upper = "[10, 255, 255]"
        elif selected_color.lower() == "green":
            lower = "[36, 25, 25]"
            upper = "[70, 255, 255]"
        elif selected_color.lower() == "blue":
            lower = "[94, 80, 2]"
            upper = "[126, 255, 255]"

        #more_colors
        elif selected_color.lower() == "yellow":
            lower = "[15, 100, 100]" #[(15, 100, 100), (35, 255, 255)],
            upper = "[35, 255, 255]"
        elif selected_color.lower() == "cyan":
            lower = "[80, 100, 100]" 
            upper = "[100, 255, 255]"
        elif selected_color.lower() == "magenta":
            lower = "[125, 100, 100]" 
            upper = "[150, 255, 255]"
        elif selected_color.lower() == "pink":
            lower = "[140, 50, 50]" 
            upper = "[170, 255, 255]"

        else:
            lower = "[0, 0, 0]"
            upper = "[0, 0, 0]"
        new_code = f'''# Feature Extraction - Extract Color from '{source}'
# Extract {selected_color} color and save in variable '{new_var}'
# Requires '{source}_rgb' from the Import Image step.
img_hsv = cv2.cvtColor({source}_rgb, cv2.COLOR_RGB2HSV)
lower_{selected_color} = np.array({lower})
upper_{selected_color} = np.array({upper})
mask = cv2.inRange(img_hsv, lower_{selected_color}, upper_{selected_color})
{new_var} = cv2.bitwise_and({source}, {source}, mask=mask)

plt.figure(figsize=(6, 6))
plt.imshow({new_var})
plt.title("Extracted {selected_color.capitalize()} from {source}")
plt.axis('off')
plt.show()
'''
        new_step = self.step.copy()
        new_step["code"] = new_code
        new_step["source"] = source
        new_step["variable"] = new_var
        new_step["color"] = selected_color
        new_step["desc"] = f"Extract Color ({selected_color}, var: {new_var}, src: {source})"
        update_step(self.idx, new_step)
        self.app.refresh_steps(get_steps())
        messagebox.showinfo("Updated", "Extract Color step updated successfully!")
        self.top.destroy()
