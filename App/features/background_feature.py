"""
Updated Background Removal Feature Module for CVTools.
Removes a specified background color from an image based on an RGB value.
Converts the image to HSV for color thresholding, then removes pixels matching the background.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

def process_background(input_image, color, tolerance=30):
    # Ensure the image is in RGB format.
    if input_image.shape[2] == 3:
        image_rgb = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
    else:
        image_rgb = input_image.copy()
    # Convert the image to HSV.
    img_hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV)
    # Convert target RGB color to HSV.
    color_array = np.uint8([[list(color)]])
    color_hsv = cv2.cvtColor(color_array, cv2.COLOR_RGB2HSV)[0][0]
    lower = np.array([max(color_hsv[0] - tolerance, 0), 50, 50])
    upper = np.array([min(color_hsv[0] + tolerance, 179), 255, 255])
    mask = cv2.inRange(img_hsv, lower, upper)
    mask_inv = cv2.bitwise_not(mask)
    output_image = cv2.bitwise_and(image_rgb, image_rgb, mask=mask_inv)
    return output_image

def generate_code(variable_name, input_variable, color, tolerance=30):
    code = f'''# Background Removal Feature
# Remove background color {color} with tolerance {tolerance}
{variable_name} = process_background({input_variable}, {color}, {tolerance})
plt.figure(figsize=(6,6))
plt.imshow({variable_name})
plt.title("Background Removed")
plt.axis("off")
plt.show()
'''
    return code
