import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from step_manager import add_step, get_steps
# Import the merge_image feature
from features import merge_image

class AddStepWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.top = tk.Toplevel(master)
        self.top.title("Add New Step")
        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(self.top, text="Select Process:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.process_var = tk.StringVar(value="Import Image")
        self.process_dropdown = ttk.Combobox(self.top, textvariable=self.process_var,
                                             values=["Import Image", "Extract Color", "Merge Image"], state="readonly")
        self.process_dropdown.grid(row=0, column=1, padx=5, pady=5)
        self.process_dropdown.bind("<<ComboboxSelected>>", self.process_change)
        
        self.frame_options = tk.Frame(self.top)
        self.frame_options.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self.process_change()
        
        tk.Button(self.top, text="Add Step", command=self.save_new_step).grid(row=2, column=0, columnspan=2, pady=10)
    
    def process_change(self, event=None):
        proc = self.process_var.get()
        for widget in self.frame_options.winfo_children():
            widget.destroy()
        if proc == "Import Image":
            tk.Label(self.frame_options, text="Variable Name:").grid(row=0, column=0, sticky='w')
            self.var_entry = tk.Entry(self.frame_options)
            self.var_entry.grid(row=0, column=1, pady=5)
        elif proc == "Extract Color":
            tk.Label(self.frame_options, text="Source Image Variable:").grid(row=0, column=0, sticky='w')
            imported = [step.get("variable") for step in get_steps() if step.get("type") == "Import Image"]
            if not imported:
                tk.Label(self.frame_options, text="(No imported images available)").grid(row=0, column=1, sticky='w')
                return
            self.src_var = tk.StringVar(value=imported[0])
            self.src_dropdown = ttk.Combobox(self.frame_options, textvariable=self.src_var,
                                             values=imported, state="readonly")
            self.src_dropdown.grid(row=0, column=1, pady=5)
            
            tk.Label(self.frame_options, text="New Variable Name:").grid(row=1, column=0, sticky='w')
            self.new_var_entry = tk.Entry(self.frame_options)
            self.new_var_entry.grid(row=1, column=1, pady=5)
            
            tk.Label(self.frame_options, text="Select Color:").grid(row=2, column=0, sticky='w')
            self.color_var = tk.StringVar(value="red")
            self.color_dropdown = ttk.Combobox(self.frame_options, textvariable=self.color_var,
                                               values=["red", "green", "blue", "yellow", "cyan", "magenta", "pink"], state="readonly")
            self.color_dropdown.grid(row=2, column=1, pady=5)
        elif proc == "Merge Image":
    # For Merge Image, let the user select two source images from all processed steps.
    # We filter out the initial (library import) step.
            available = [step.get("variable") for step in get_steps() if step.get("type") != "initial" and step.get("variable")]
            tk.Label(self.frame_options, text="Source Image Variable 1:").grid(row=0, column=0, sticky='w')
            self.src1_var = tk.StringVar(value=available[0])
            self.src1_dropdown = ttk.Combobox(self.frame_options, textvariable=self.src1_var,
                                            values=available, state="readonly")
            self.src1_dropdown.grid(row=0, column=1, pady=5)
            
            tk.Label(self.frame_options, text="Source Image Variable 2:").grid(row=1, column=0, sticky='w')
            self.src2_var = tk.StringVar(value=available[1])
            self.src2_dropdown = ttk.Combobox(self.frame_options, textvariable=self.src2_var,
                                            values=available, state="readonly")
            self.src2_dropdown.grid(row=1, column=1, pady=5)
            
            tk.Label(self.frame_options, text="New Variable Name:").grid(row=2, column=0, sticky='w')
            self.merge_var_entry = tk.Entry(self.frame_options)
            self.merge_var_entry.grid(row=2, column=1, pady=5)

            

    
    def save_new_step(self):
        proc = self.process_var.get()
        if proc == "Import Image":
            var_name = self.var_entry.get().strip()
            if not var_name:
                messagebox.showerror("Error", "Variable name cannot be empty.")
                return
            file_path = filedialog.askopenfilename(
                title="Select an Image",
                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
            )
            if not file_path:
                messagebox.showerror("Error", "No file selected.")
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
            step = {
                "code": new_code,
                "desc": f"Import Image (var: {var_name}, file: {file_path})",
                "type": "Import Image",
                "variable": var_name,
                "file_path": file_path
            }
            add_step(step)
            self.app.refresh_steps(get_steps())
            messagebox.showinfo("Step Added", "Import Image step added successfully!")
            self.top.destroy()
        elif proc == "Extract Color":
            imported = [step.get("variable") for step in get_steps() if step.get("type") == "Import Image"]
            if not imported:
                messagebox.showerror("Error", "No imported images available. Add an Import Image step first.")
                return
            src_image = self.src_var.get().strip()
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
            #---
            else:
                lower = "[0, 0, 0]"
                upper = "[0, 0, 0]"
            new_code = f'''# Feature Extraction - Extract Color from '{src_image}'
# Extract {selected_color} color and save in variable '{new_var}'
# Requires '{src_image}_rgb' from the Import Image step.
img_hsv = cv2.cvtColor({src_image}_rgb, cv2.COLOR_RGB2HSV)
lower_{selected_color} = np.array({lower})
upper_{selected_color} = np.array({upper})
mask = cv2.inRange(img_hsv, lower_{selected_color}, upper_{selected_color})
{new_var} = cv2.bitwise_and({src_image}, {src_image}, mask=mask)

plt.figure(figsize=(6, 6))
plt.imshow({new_var})
plt.title("Extracted {selected_color.capitalize()} from {src_image}")
plt.axis('off')
plt.show()
'''
            step = {
                "code": new_code,
                "desc": f"Extract Color ({selected_color}, var: {new_var}, src: {src_image})",
                "type": "Extract Color",
                "source": src_image,
                "variable": new_var,
                "color": selected_color
            }
            add_step(step)
            self.app.refresh_steps(get_steps())
            messagebox.showinfo("Step Added", "Extract Color step added successfully!")
            self.top.destroy()
        elif proc == "Merge Image":
            imported = [step.get("variable") for step in get_steps() if step.get("type") == "Import Image"]
            if len(imported) < 1:
                messagebox.showerror("Error", "At least one imported images are required to merge.")
                return
            src1 = self.src1_var.get().strip()
            src2 = self.src2_var.get().strip()
            new_var = self.merge_var_entry.get().strip()
            if not new_var:
                messagebox.showerror("Error", "New variable name cannot be empty.")
                return
            # Use the merge_image feature to generate the code cell.
            new_code = merge_image.generate_code(new_var, src1, src2)
            step = {
                "code": new_code,
                "desc": f"Merge Image (var: {new_var}, src1: {src1}, src2: {src2})",
                "type": "Merge Image",
                "source1": src1,
                "source2": src2,
                "variable": new_var
            }
            add_step(step)
            self.app.refresh_steps(get_steps())
            messagebox.showinfo("Step Added", "Merge Image step added successfully!")
            self.top.destroy()
