"""
Updated Image Recognition Feature Module for CVTools.
Supports Template Matching and Face Detection.
For Template Matching, ensure that the template image is preloaded in your notebook.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

def process_recognition(input_image, method, params):
    output_image = input_image.copy()
    
    if method.lower() == "template_matching":
        # Parameters: template (variable name must reference an existing template), tm_method
        template = params.get("template")
        if template is None:
            return output_image
        tm_method = getattr(cv2, params.get("tm_method", "TM_CCOEFF"), cv2.TM_CCOEFF)
        res = cv2.matchTemplate(input_image, template, tm_method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        h, w = template.shape[:2]
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(output_image, top_left, bottom_right, (0, 0, 255), 2)
    
    elif method.lower() == "face_detection":
        # Parameters: scaleFactor, minNeighbors
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
        scaleFactor = float(params.get("scaleFactor", 1.1))
        minNeighbors = int(params.get("minNeighbors", 5))
        faces = face_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors)
        for (x, y, w, h) in faces:
            cv2.rectangle(output_image, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    return output_image

def generate_code(variable_name, input_variable, method, params):
    params_str = ", ".join([f'"{k}": {v}' for k, v in params.items()])
    code = f'''# Image Recognition Feature: {method.capitalize()}
params = {{{params_str}}}
{variable_name} = process_recognition({input_variable}, "{method}", params)
plt.figure(figsize=(6,6))
plt.imshow({variable_name})
plt.title("{method.capitalize()} Recognition")
plt.axis("off")
plt.show()
'''
    return code
