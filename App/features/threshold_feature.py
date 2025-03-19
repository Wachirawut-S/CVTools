"""
Template for thresholding features in CVTools.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

def process_threshold(input_image, thresh_value, max_value, method):
    """
    Apply thresholding on the input image.
    
    Parameters:
        input_image: Input grayscale image (NumPy array).
        thresh_value: The threshold value.
        max_value: The maximum value to use with the THRESH_BINARY methods.
        method: One of the cv2 thresholding methods.
        
    Returns:
        output_image: The thresholded image.
    """
    # Method can be cv2.THRESH_BINARY, cv2.THRESH_BINARY_INV, etc.
    _, output_image = cv2.threshold(input_image, thresh_value, max_value, method)
    return output_image

def generate_code(variable_name, input_variable, thresh_value, max_value, method):
    """
    Generate code for the threshold feature.
    
    Parameters:
        variable_name: The variable to store output image.
        input_variable: The variable with the input image.
        thresh_value: Threshold value.
        max_value: Maximum value.
        method: Thresholding method (as string).
    
    Returns:
        code: A string representing the code cell.
    """
    # Map method string to cv2 constant
    method_map = {
        "THRESH_BINARY": "cv2.THRESH_BINARY",
        "THRESH_BINARY_INV": "cv2.THRESH_BINARY_INV",
        "THRESH_TRUNC": "cv2.THRESH_TRUNC",
        "THRESH_TOZERO": "cv2.THRESH_TOZERO",
        "THRESH_TOZERO_INV": "cv2.THRESH_TOZERO_INV"
    }
    cv_method = method_map.get(method, "cv2.THRESH_BINARY")
    code = f'''# Threshold Feature
# Apply {method} on image {input_variable}
{variable_name} = cv2.threshold({input_variable}, {thresh_value}, {max_value}, {cv_method})[1]
plt.figure(figsize=(6, 6))
plt.imshow({variable_name}, cmap='gray')
plt.title("Thresholded Output ({method})")
plt.axis('off')
plt.show()
'''
    return code
