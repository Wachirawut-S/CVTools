# features/extract_color.py

def generate_code(new_var, src_image, selected_color):
    """
    Generate the code cell to extract a specific color from an image.
    
    Parameters:
        new_var (str): The variable name to store the processed image.
        src_image (str): The source image variable name (from an Import Image step).
        selected_color (str): The color to extract ('red', 'green', 'blue', 'yellow', 'cyan', 'magenta' or 'pink').
        
    Returns:
        str: A string representing the code cell.
    """
    if selected_color.lower() == "red":
        lower = "[94, 80, 2]"
        upper = "[126, 255, 255]"
    elif selected_color.lower() == "green":
        lower = "[36, 25, 25]"
        upper = "[70, 255, 255]"
    elif selected_color.lower() == "blue":
        lower = "[0, 120, 70]"
        upper = "[10, 255, 255]"
    elif selected_color.lower() == "yellow":
        lower = "[15, 100, 100]"
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
        
    code = f'''# Feature Extraction - Extract Color from '{src_image}'
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
    return code
