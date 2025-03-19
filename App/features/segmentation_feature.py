"""
Updated Image Segmentation Feature Module for CVTools.
Supports basic segmentation via thresholding, distance transforms, and contour detection.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

def process_segmentation(input_image, method, params):
    output_image = input_image.copy()
    
    if method.lower() == "basic":
        gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
        thresh_val = int(params.get("thresh", 127))
        ret, output_image = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
    
    elif method.lower() == "distance_transform":
        gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        output_image = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
    
    elif method.lower() == "contours":
        gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, int(params.get("thresh", 127)), 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(output_image, contours, -1, (0, 255, 0), 2)
    
    return output_image

def generate_code(variable_name, input_variable, method, params):
    params_str = ", ".join([f'"{k}": {v}' for k, v in params.items()])
    code = f'''# Image Segmentation Feature: {method.capitalize()}
params = {{{params_str}}}
{variable_name} = process_segmentation({input_variable}, "{method}", params)
plt.figure(figsize=(6,6))
plt.imshow({variable_name}, cmap="gray")
plt.title("{method.capitalize()} Segmentation")
plt.axis("off")
plt.show()
'''
    return code
