# features/merge_image.py
import cv2
import numpy as np
import matplotlib.pyplot as plt

def generate_code(new_var, img1_var, img2_var):
    """
    Generate the code cell to merge two processed images using bitwise OR.
    
    Parameters:
        new_var (str): The new variable name for the merged image.
        img1_var (str): The first image variable (e.g., extracted red).
        img2_var (str): The second image variable (e.g., extracted blue).
        
    Returns:
        str: A string representing the code cell.
    """
    code = f'''# Merge Image - Combining '{img1_var}' and '{img2_var}'
{new_var} = cv2.bitwise_or({img1_var}, {img2_var})

plt.figure(figsize=(6,6))
plt.imshow(cv2.cvtColor({new_var}, cv2.COLOR_BGR2RGB))
plt.title("Merged Image - {img1_var} + {img2_var}")
plt.axis('off')
plt.show()
'''
    return code
