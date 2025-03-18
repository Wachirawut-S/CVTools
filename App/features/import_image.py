# features/import_image.py

def generate_code(var_name, file_path):
    """
    Generate the code cell to import an image.
    
    Parameters:
        var_name (str): The variable name to store the image.
        file_path (str): The file path of the image.
        
    Returns:
        str: A string representing the code cell.
    """
    code = f'''# Import Image for variable '{var_name}'
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
    return code
