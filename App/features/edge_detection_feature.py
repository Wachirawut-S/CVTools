"""
Edge Detection Feature Module for CVTools.
Supports 2D kernel filtering (Blur, Sharpen, Gaussian) and edge detection (Laplacian, Prewitt, Sobel, Canny).
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

def process_edge_detection(input_image, method, params):
    output_image = input_image.copy()
    
    if method.lower() in ["blur", "gaussian"]:
        ksize = int(params.get("ksize", 3))
        sigma = float(params.get("sigma", 0))
        if method.lower() == "blur":
            output_image = cv2.blur(input_image, (ksize, ksize))
        else:
            output_image = cv2.GaussianBlur(input_image, (ksize, ksize), sigma)
    
    elif method.lower() == "sharpen":
        # A common sharpening kernel.
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        output_image = cv2.filter2D(input_image, -1, kernel)
    
    elif method.lower() == "laplacian":
        ksize = int(params.get("ksize", 3))
        output_image = cv2.Laplacian(input_image, cv2.CV_64F, ksize=ksize)
    
    elif method.lower() == "prewitt":
        kernelx = np.array([[1, 0, -1],
                            [1, 0, -1],
                            [1, 0, -1]])
        kernely = np.array([[1, 1, 1],
                            [0, 0, 0],
                            [-1, -1, -1]])
        grad_x = cv2.filter2D(input_image, cv2.CV_64F, kernelx)
        grad_y = cv2.filter2D(input_image, cv2.CV_64F, kernely)
        output_image = cv2.magnitude(grad_x, grad_y)
    
    elif method.lower() == "sobel":
        ksize = int(params.get("ksize", 3))
        grad_x = cv2.Sobel(input_image, cv2.CV_64F, 1, 0, ksize=ksize)
        grad_y = cv2.Sobel(input_image, cv2.CV_64F, 0, 1, ksize=ksize)
        output_image = cv2.magnitude(grad_x, grad_y)
    
    elif method.lower() == "canny":
        threshold1 = float(params.get("threshold1", 100))
        threshold2 = float(params.get("threshold2", 200))
        output_image = cv2.Canny(input_image, threshold1, threshold2)
    
    return output_image

def generate_code(variable_name, input_variable, method, params):
    params_str = ", ".join([f'"{k}": {v}' for k, v in params.items()])
    code = f'''# Edge Detection Feature: {method.capitalize()}
params = {{{params_str}}}
{variable_name} = process_edge_detection({input_variable}, "{method}", params)
plt.figure(figsize=(6,6))
plt.imshow({variable_name}, cmap="gray")
plt.title("{method.capitalize()} Edge Detection")
plt.axis("off")
plt.show()
'''
    return code
