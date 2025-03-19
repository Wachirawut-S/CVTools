import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from step_manager import add_step, get_steps

# Import feature modules
from features import merge_image
import features.threshold_feature as threshold_feature
import features.transform_feature as transform_feature
import features.reconstruction_feature as reconstruction_feature
import features.segmentation_feature as segmentation_feature
import features.recognition_feature as recognition_feature
import features.background_feature as background_feature
# import features.new_feature_template as new_feature_template  # optional

class AddStepWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.top = tk.Toplevel(master)
        self.top.title("Add New Step")
        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(self.top, text="Select Process:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        # Updated process options
        self.process_var = tk.StringVar(value="Import Image")
        self.process_dropdown = ttk.Combobox(self.top, textvariable=self.process_var,
                                             values=["Import Image", "Extract Color", "Merge Image", 
                                                     "Threshold", "Transformation", "Edge Detection",
                                                     "Image Reconstruction", "Image Segmentation", "Image Recognition", 
                                                     "Background Removal", "New feature"],
                                             state="readonly")
        self.process_dropdown.grid(row=0, column=1, padx=5, pady=5)
        self.process_dropdown.bind("<<ComboboxSelected>>", self.process_change)
        
        self.frame_options = tk.Frame(self.top)
        self.frame_options.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self.process_change()
        
        tk.Button(self.top, text="Add Step", command=self.save_new_step).grid(row=2, column=0, columnspan=2, pady=10)
    
    def process_change(self, event=None):
        proc = self.process_var.get()
        # Clear any existing widgets in the options frame.
        for widget in self.frame_options.winfo_children():
            widget.destroy()
        
        if proc == "Import Image":
            tk.Label(self.frame_options, text="Variable Name:").grid(row=0, column=0, sticky='w')
            self.var_entry = tk.Entry(self.frame_options)
            self.var_entry.grid(row=0, column=1, pady=5)
            tk.Label(self.frame_options, text="Choose Output Format:").grid(row=1, column=0, sticky='w')
            self.format_var = tk.StringVar(value="RGB")
            self.format_dropdown = ttk.Combobox(self.frame_options, textvariable=self.format_var,
                                                values=["RGB", "Gray"], state="readonly")
            self.format_dropdown.grid(row=1, column=1, pady=5)
        
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
                                               values=["red", "green", "blue", "yellow", "cyan", "magenta", "pink"],
                                               state="readonly")
            self.color_dropdown.grid(row=2, column=1, pady=5)
        
        elif proc == "Merge Image":
            available = [step.get("variable") for step in get_steps() if step.get("type") == "Import Image"]
            tk.Label(self.frame_options, text="Source Image Variable 1:").grid(row=0, column=0, sticky='w')
            self.src1_var = tk.StringVar(value=available[0] if available else "")
            self.src1_dropdown = ttk.Combobox(self.frame_options, textvariable=self.src1_var,
                                              values=available, state="readonly")
            self.src1_dropdown.grid(row=0, column=1, pady=5)
            tk.Label(self.frame_options, text="Source Image Variable 2:").grid(row=1, column=0, sticky='w')
            self.src2_var = tk.StringVar(value=available[1] if len(available) > 1 else available[0])
            self.src2_dropdown = ttk.Combobox(self.frame_options, textvariable=self.src2_var,
                                              values=available, state="readonly")
            self.src2_dropdown.grid(row=1, column=1, pady=5)
            tk.Label(self.frame_options, text="New Variable Name:").grid(row=2, column=0, sticky='w')
            self.merge_var_entry = tk.Entry(self.frame_options)
            self.merge_var_entry.grid(row=2, column=1, pady=5)
        
        elif proc == "Threshold":
            tk.Label(self.frame_options, text="Input Image Variable:").grid(row=0, column=0, sticky='w')
            imported = [step.get("variable") for step in get_steps() if step.get("type") == "Import Image"]
            self.src_var = tk.StringVar(value=imported[0] if imported else "")
            self.src_dropdown = ttk.Combobox(self.frame_options, textvariable=self.src_var,
                                             values=imported, state="readonly")
            self.src_dropdown.grid(row=0, column=1, pady=5)
            tk.Label(self.frame_options, text="New Variable Name:").grid(row=1, column=0, sticky='w')
            self.new_var_entry = tk.Entry(self.frame_options)
            self.new_var_entry.grid(row=1, column=1, pady=5)
            tk.Label(self.frame_options, text="Threshold Value:").grid(row=2, column=0, sticky='w')
            self.thresh_entry = tk.Entry(self.frame_options)
            self.thresh_entry.grid(row=2, column=1, pady=5)
            tk.Label(self.frame_options, text="Max Value:").grid(row=3, column=0, sticky='w')
            self.max_entry = tk.Entry(self.frame_options)
            self.max_entry.grid(row=3, column=1, pady=5)
            tk.Label(self.frame_options, text="Method:").grid(row=4, column=0, sticky='w')
            self.method_var = tk.StringVar(value="THRESH_BINARY")
            self.method_dropdown = ttk.Combobox(self.frame_options, textvariable=self.method_var,
                                                values=["THRESH_BINARY", "THRESH_BINARY_INV", "THRESH_TRUNC",
                                                        "THRESH_TOZERO", "THRESH_TOZERO_INV"], state="readonly")
            self.method_dropdown.grid(row=4, column=1, pady=5)
        
        elif proc == "Transformation":
            tk.Label(self.frame_options, text="Input Image Variable:").grid(row=0, column=0, sticky='w')
            imported = [step.get("variable") for step in get_steps() if step.get("type") == "Import Image"]
            self.src_var = tk.StringVar(value=imported[0] if imported else "")
            self.src_dropdown = ttk.Combobox(self.frame_options, textvariable=self.src_var,
                                             values=imported, state="readonly")
            self.src_dropdown.grid(row=0, column=1, pady=5)
            tk.Label(self.frame_options, text="New Variable Name:").grid(row=1, column=0, sticky='w')
            self.new_var_entry = tk.Entry(self.frame_options)
            self.new_var_entry.grid(row=1, column=1, pady=5)
            
            # Transformation type dropdown with updated options
            tk.Label(self.frame_options, text="Transformation Type:").grid(row=2, column=0, sticky='w')
            self.trans_type_var = tk.StringVar(value="translation")
            self.trans_dropdown = ttk.Combobox(self.frame_options, textvariable=self.trans_type_var,
                                               values=["translation", "scaling", "rotate", "shear", 
                                                       "affine", "perspective", "resize", "cropping"],
                                               state="readonly")
            self.trans_dropdown.grid(row=2, column=1, pady=5)
            self.trans_dropdown.bind("<<ComboboxSelected>>", self.update_trans_hint)
            
            self.trans_hint = tk.Label(self.frame_options, text="Enter parameters as key=value, comma separated")
            self.trans_hint.grid(row=3, column=0, columnspan=2, sticky='w')
            self.trans_params_entry = tk.Entry(self.frame_options)
            self.trans_params_entry.grid(row=4, column=0, columnspan=2, pady=5)
        
        elif proc == "Edge Detection":
            tk.Label(self.frame_options, text="Input Image Variable:").grid(row=0, column=0, sticky='w')
            imported = [step.get("variable") for step in get_steps() if step.get("type") == "Import Image"]
            self.src_var = tk.StringVar(value=imported[0] if imported else "")
            self.src_dropdown = ttk.Combobox(self.frame_options, textvariable=self.src_var,
                                             values=imported, state="readonly")
            self.src_dropdown.grid(row=0, column=1, pady=5)
            tk.Label(self.frame_options, text="New Variable Name:").grid(row=1, column=0, sticky='w')
            self.new_var_entry = tk.Entry(self.frame_options)
            self.new_var_entry.grid(row=1, column=1, pady=5)
            
            tk.Label(self.frame_options, text="Edge Detection Method:").grid(row=2, column=0, sticky='w')
            self.edge_method_var = tk.StringVar(value="canny")
            self.edge_dropdown = ttk.Combobox(self.frame_options, textvariable=self.edge_method_var,
                                              values=["blur", "gaussian", "sharpen", "laplacian",
                                                      "prewitt", "sobel", "canny"],
                                              state="readonly")
            self.edge_dropdown.grid(row=2, column=1, pady=5)
            tk.Label(self.frame_options, text="Parameters (key=value comma separated):").grid(row=3, column=0, sticky='w')
            self.edge_params_entry = tk.Entry(self.frame_options)
            self.edge_params_entry.grid(row=3, column=1, pady=5)
        
        elif proc == "Image Reconstruction":
            tk.Label(self.frame_options, text="Input Image Variable:").grid(row=0, column=0, sticky='w')
            imported = [step.get("variable") for step in get_steps() if step.get("type") == "Import Image"]
            self.src_var = tk.StringVar(value=imported[0] if imported else "")
            self.src_dropdown = ttk.Combobox(self.frame_options, textvariable=self.src_var,
                                             values=imported, state="readonly")
            self.src_dropdown.grid(row=0, column=1, pady=5)
            tk.Label(self.frame_options, text="New Variable Name:").grid(row=1, column=0, sticky='w')
            self.new_var_entry = tk.Entry(self.frame_options)
            self.new_var_entry.grid(row=1, column=1, pady=5)
            tk.Label(self.frame_options, text="Reconstruction Type:").grid(row=2, column=0, sticky='w')
            self.rec_type_var = tk.StringVar(value="hough_line")
            self.rec_dropdown = ttk.Combobox(self.frame_options, textvariable=self.rec_type_var,
                                             values=["dilation", "erosion", "opening", "closing", "gradient",
                                                     "tophat", "blackhat", "hough_line", "hough_circle"],
                                             state="readonly")
            self.rec_dropdown.grid(row=2, column=1, pady=5)
            tk.Label(self.frame_options, text="Parameters (key=value comma separated):").grid(row=3, column=0, sticky='w')
            self.rec_params_entry = tk.Entry(self.frame_options)
            self.rec_params_entry.grid(row=3, column=1, pady=5)
        
        elif proc == "Image Segmentation":
            tk.Label(self.frame_options, text="Input Image Variable:").grid(row=0, column=0, sticky='w')
            imported = [step.get("variable") for step in get_steps() if step.get("type") == "Import Image"]
            self.src_var = tk.StringVar(value=imported[0] if imported else "")
            self.src_dropdown = ttk.Combobox(self.frame_options, textvariable=self.src_var,
                                             values=imported, state="readonly")
            self.src_dropdown.grid(row=0, column=1, pady=5)
            tk.Label(self.frame_options, text="New Variable Name:").grid(row=1, column=0, sticky='w')
            self.new_var_entry = tk.Entry(self.frame_options)
            self.new_var_entry.grid(row=1, column=1, pady=5)
            tk.Label(self.frame_options, text="Segmentation Type:").grid(row=2, column=0, sticky='w')
            self.seg_type_var = tk.StringVar(value="contours")
            self.seg_dropdown = ttk.Combobox(self.frame_options, textvariable=self.seg_type_var,
                                             values=["basic", "distance_transform", "contours"],
                                             state="readonly")
            self.seg_dropdown.grid(row=2, column=1, pady=5)
            tk.Label(self.frame_options, text="Parameters (key=value comma separated):").grid(row=3, column=0, sticky='w')
            self.seg_params_entry = tk.Entry(self.frame_options)
            self.seg_params_entry.grid(row=3, column=1, pady=5)
        
        elif proc == "Image Recognition":
            tk.Label(self.frame_options, text="Input Image Variable:").grid(row=0, column=0, sticky='w')
            imported = [step.get("variable") for step in get_steps() if step.get("type") == "Import Image"]
            self.src_var = tk.StringVar(value=imported[0] if imported else "")
            self.src_dropdown = ttk.Combobox(self.frame_options, textvariable=self.src_var,
                                             values=imported, state="readonly")
            self.src_dropdown.grid(row=0, column=1, pady=5)
            tk.Label(self.frame_options, text="New Variable Name:").grid(row=1, column=0, sticky='w')
            self.new_var_entry = tk.Entry(self.frame_options)
            self.new_var_entry.grid(row=1, column=1, pady=5)
            tk.Label(self.frame_options, text="Recognition Type:").grid(row=2, column=0, sticky='w')
            self.recog_type_var = tk.StringVar(value="face_detection")
            self.recog_dropdown = ttk.Combobox(self.frame_options, textvariable=self.recog_type_var,
                                               values=["face_detection", "template_matching"],
                                               state="readonly")
            self.recog_dropdown.grid(row=2, column=1, pady=5)
            tk.Label(self.frame_options, text="Parameters (key=value comma separated):").grid(row=3, column=0, sticky='w')
            self.recog_params_entry = tk.Entry(self.frame_options)
            self.recog_params_entry.grid(row=3, column=1, pady=5)
        
        elif proc == "Background Removal":
            tk.Label(self.frame_options, text="Input Image Variable:").grid(row=0, column=0, sticky='w')
            imported = [step.get("variable") for step in get_steps() if step.get("type") == "Import Image"]
            self.src_var = tk.StringVar(value=imported[0] if imported else "")
            self.src_dropdown = ttk.Combobox(self.frame_options, textvariable=self.src_var,
                                             values=imported, state="readonly")
            self.src_dropdown.grid(row=0, column=1, pady=5)
            tk.Label(self.frame_options, text="New Variable Name:").grid(row=1, column=0, sticky='w')
            self.new_var_entry = tk.Entry(self.frame_options)
            self.new_var_entry.grid(row=1, column=1, pady=5)
            tk.Label(self.frame_options, text="Color to Remove (RGB tuple):").grid(row=2, column=0, sticky='w')
            self.bg_color_entry = tk.Entry(self.frame_options)
            self.bg_color_entry.insert(0, "(255,255,255)")
            self.bg_color_entry.grid(row=2, column=1, pady=5)
            tk.Label(self.frame_options, text="Tolerance:").grid(row=3, column=0, sticky='w')
            self.tolerance_entry = tk.Entry(self.frame_options)
            self.tolerance_entry.insert(0, "30")
            self.tolerance_entry.grid(row=3, column=1, pady=5)
        
        elif proc == "New feature":
            tk.Label(self.frame_options, text="This is a placeholder for new features.").grid(row=0, column=0, sticky='w')
    
    def update_trans_hint(self, event=None):
        # Update the hint text based on selected transformation type.
        t_type = self.trans_type_var.get()
        hint = ""
        if t_type == "translation":
            hint = "Enter tx and ty (e.g., tx=10,ty=20)"
        elif t_type == "scaling":
            hint = "Enter sx and sy (e.g., sx=1.5,sy=1.5)"
        elif t_type == "rotate":
            hint = "Enter degree (e.g., degree=45)"
        elif t_type == "shear":
            hint = "Enter shear_x and shear_y (e.g., shear_x=0.2,shear_y=0.1)"
        elif t_type == "affine":
            hint = ("Enter source points and destination points; "
                    "format: src=x0,y0;x1,y1;x2,y2, dst=x0,y0;x1,y1;x2,y2")
        elif t_type == "perspective":
            hint = ("Enter source and destination 4 points; "
                    "format: src=x0,y0;x1,y1;x2,y2;x3,y3, dst=x0,y0;x1,y1;x2,y2;x3,y3")
        elif t_type == "resize":
            hint = "Enter width and height (e.g., width=300,height=200)"
        elif t_type == "cropping":
            hint = "Enter x, y, width and height (e.g., x=10,y=20,width=100,height=100)"
        else:
            hint = "Enter parameters as key=value, comma separated"
        self.trans_hint.config(text=hint)
    
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
            output_format = self.format_var.get()
            if output_format == "RGB":
                new_code = f'''# Import Image for variable '{var_name}'
file_path = r"{file_path}"
{var_name} = cv2.imread(file_path)
{var_name}_rgb = cv2.cvtColor({var_name}, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(15,5))
plt.subplot(1,2,1)
plt.title("Original - {var_name}")
plt.imshow(cv2.cvtColor({var_name}, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
'''
            else:
                new_code = f'''# Import Image for variable '{var_name}'
file_path = r"{file_path}"
{var_name} = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

plt.figure(figsize=(6,6))
plt.title("Grayscale - {var_name}")
plt.imshow({var_name}, cmap='gray')
plt.axis('off')
plt.show()
'''
            step = {
                "code": new_code,
                "desc": f"Import Image (var: {var_name}, file: {file_path}, format: {output_format})",
                "type": "Import Image",
                "variable": var_name,
                "file_path": file_path,
                "format": output_format
            }
            add_step(step)
        
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
                lower, upper = "[0, 120, 70]", "[10, 255, 255]"
            elif selected_color.lower() == "green":
                lower, upper = "[36, 25, 25]", "[70, 255, 255]"
            elif selected_color.lower() == "blue":
                lower, upper = "[94, 80, 2]", "[126, 255, 255]"
            elif selected_color.lower() == "yellow":
                lower, upper = "[15, 100, 100]", "[35, 255, 255]"
            elif selected_color.lower() == "cyan":
                lower, upper = "[80, 100, 100]", "[100, 255, 255]"
            elif selected_color.lower() == "magenta":
                lower, upper = "[125, 100, 100]", "[150, 255, 255]"
            elif selected_color.lower() == "pink":
                lower, upper = "[140, 50, 50]", "[170, 255, 255]"
            else:
                lower, upper = "[0, 0, 0]", "[0, 0, 0]"
            new_code = f'''# Feature Extraction - Extract Color from '{src_image}'
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
        
        elif proc == "Merge Image":
            imported = [step.get("variable") for step in get_steps() if step.get("type") == "Import Image"]
            if len(imported) < 1:
                messagebox.showerror("Error", "At least one imported image is required to merge.")
                return
            src1 = self.src1_var.get().strip()
            src2 = self.src2_var.get().strip()
            new_var = self.merge_var_entry.get().strip()
            if not new_var:
                messagebox.showerror("Error", "New variable name cannot be empty.")
                return
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
        
        elif proc == "Threshold":
            imported = [step.get("variable") for step in get_steps() if step.get("type") == "Import Image"]
            if not imported:
                messagebox.showerror("Error", "No imported images available for thresholding.")
                return
            src_image = self.src_var.get().strip()
            new_var = self.new_var_entry.get().strip()
            thresh_value = self.thresh_entry.get().strip()
            max_value = self.max_entry.get().strip()
            method = self.method_var.get().strip()
            if not new_var or not thresh_value or not max_value:
                messagebox.showerror("Error", "All fields are required for thresholding.")
                return
            new_code = threshold_feature.generate_code(new_var, src_image, thresh_value, max_value, method)
            step = {
                "code": new_code,
                "desc": f"Threshold ({method}, var: {new_var}, src: {src_image})",
                "type": "Threshold",
                "source": src_image,
                "variable": new_var,
                "thresh": thresh_value,
                "max": max_value,
                "method": method
            }
            add_step(step)
        
        elif proc == "Transformation":
            imported = [step.get("variable") for step in get_steps() if step.get("type") == "Import Image"]
            if not imported:
                messagebox.showerror("Error", "No imported images available for transformation.")
                return
            src_image = self.src_var.get().strip()
            new_var = self.new_var_entry.get().strip()
            trans_type = self.trans_type_var.get().strip()
            params_str = self.trans_params_entry.get().strip()
            params = dict(item.split('=') for item in params_str.split(',')) if params_str else {}
            new_code = transform_feature.generate_code(new_var, src_image, trans_type, params)
            step = {
                "code": new_code,
                "desc": f"Transformation ({trans_type}, var: {new_var}, src: {src_image})",
                "type": "Transformation",
                "source": src_image,
                "variable": new_var,
                "transformation": trans_type,
                "params": params
            }
            add_step(step)
        
        elif proc == "Edge Detection":
            imported = [step.get("variable") for step in get_steps() if step.get("type") == "Import Image"]
            if not imported:
                messagebox.showerror("Error", "No imported images available for edge detection.")
                return
            src_image = self.src_var.get().strip()
            new_var = self.new_var_entry.get().strip()
            edge_method = self.edge_method_var.get().strip()
            params_str = self.edge_params_entry.get().strip()
            params = dict(item.split('=') for item in params_str.split(',')) if params_str else {}
            new_code =  features.edge_detection_feature.generate_code(new_var, src_image, edge_method, params)
            step = {
                "code": new_code,
                "desc": f"Edge Detection ({edge_method}, var: {new_var}, src: {src_image})",
                "type": "Edge Detection",
                "source": src_image,
                "variable": new_var,
                "edge_method": edge_method,
                "params": params
            }
            add_step(step)
        
        elif proc == "Image Reconstruction":
            imported = [step.get("variable") for step in get_steps() if step.get("type") == "Import Image"]
            if not imported:
                messagebox.showerror("Error", "No imported images available for reconstruction.")
                return
            src_image = self.src_var.get().strip()
            new_var = self.new_var_entry.get().strip()
            rec_type = self.rec_type_var.get().strip()
            params_str = self.rec_params_entry.get().strip()
            params = dict(item.split('=') for item in params_str.split(',')) if params_str else {}
            new_code = reconstruction_feature.generate_code(new_var, src_image, rec_type, **params)
            step = {
                "code": new_code,
                "desc": f"Image Reconstruction ({rec_type}, var: {new_var}, src: {src_image})",
                "type": "Image Reconstruction",
                "source": src_image,
                "variable": new_var,
                "reconstruction": rec_type,
                "params": params
            }
            add_step(step)
        
        elif proc == "Image Segmentation":
            imported = [step.get("variable") for step in get_steps() if step.get("type") == "Import Image"]
            if not imported:
                messagebox.showerror("Error", "No imported images available for segmentation.")
                return
            src_image = self.src_var.get().strip()
            new_var = self.new_var_entry.get().strip()
            seg_type = self.seg_type_var.get().strip()
            params_str = self.seg_params_entry.get().strip()
            params = dict(item.split('=') for item in params_str.split(',')) if params_str else {}
            new_code = segmentation_feature.generate_code(new_var, src_image, seg_type, **params)
            step = {
                "code": new_code,
                "desc": f"Image Segmentation ({seg_type}, var: {new_var}, src: {src_image})",
                "type": "Image Segmentation",
                "source": src_image,
                "variable": new_var,
                "segmentation": seg_type,
                "params": params
            }
            add_step(step)
        
        elif proc == "Image Recognition":
            imported = [step.get("variable") for step in get_steps() if step.get("type") == "Import Image"]
            if not imported:
                messagebox.showerror("Error", "No imported images available for recognition.")
                return
            src_image = self.src_var.get().strip()
            new_var = self.new_var_entry.get().strip()
            recog_type = self.recog_type_var.get().strip()
            params_str = self.recog_params_entry.get().strip()
            params = dict(item.split('=') for item in params_str.split(',')) if params_str else {}
            new_code = recognition_feature.generate_code(new_var, src_image, recog_type, **params)
            step = {
                "code": new_code,
                "desc": f"Image Recognition ({recog_type}, var: {new_var}, src: {src_image})",
                "type": "Image Recognition",
                "source": src_image,
                "variable": new_var,
                "recognition": recog_type,
                "params": params
            }
            add_step(step)
        
        elif proc == "Background Removal":
            imported = [step.get("variable") for step in get_steps() if step.get("type") == "Import Image"]
            if not imported:
                messagebox.showerror("Error", "No imported images available for background removal.")
                return
            src_image = self.src_var.get().strip()
            new_var = self.new_var_entry.get().strip()
            try:
                color = eval(self.bg_color_entry.get().strip())
            except Exception:
                messagebox.showerror("Error", "Invalid RGB tuple for color.")
                return
            tolerance = self.tolerance_entry.get().strip()
            new_code = background_feature.generate_code(new_var, src_image, color, tolerance)
            step = {
                "code": new_code,
                "desc": f"Background Removal (var: {new_var}, src: {src_image}, color: {color})",
                "type": "Background Removal",
                "source": src_image,
                "variable": new_var,
                "color": color,
                "tolerance": tolerance
            }
            add_step(step)
        
        # elif proc == "New feature":
        #     new_code = new_feature_template.generate_code("new_var", "input_image")
        #     step = {
        #         "code": new_code,
        #         "desc": "New feature placeholder",
        #         "type": "New feature",
        #         "variable": "new_var"
        #     }
        #     add_step(step)
        
        self.app.refresh_steps(get_steps())
        messagebox.showinfo("Step Added", f"{proc} step added successfully!")
        self.top.destroy()
