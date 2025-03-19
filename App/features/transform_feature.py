"""
Updated Transformation Feature Module for CVTools.
Supported methods: translation, scaling, rotate, shear, affine, perspective, resize, cropping.
Each method uses specific parameters.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

def process_transformation(input_image, transformation_type, params):
    output_image = input_image.copy()
    
    if transformation_type == "translation":
        # Parameters: tx, ty
        tx = float(params.get("tx", 0))
        ty = float(params.get("ty", 0))
        M = np.float32([[1, 0, tx], [0, 1, ty]])
        output_image = cv2.warpAffine(input_image, M, (input_image.shape[1], input_image.shape[0]))
    
    elif transformation_type == "scaling":
        # Parameters: sx, sy (scaling factors)
        sx = float(params.get("sx", 1.0))
        sy = float(params.get("sy", 1.0))
        output_image = cv2.resize(input_image, None, fx=sx, fy=sy)
    
    elif transformation_type == "rotate":
        # Parameter: degree
        degree = float(params.get("degree", 0))
        (h, w) = input_image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, degree, 1.0)
        output_image = cv2.warpAffine(input_image, M, (w, h))
    
    elif transformation_type == "shear":
        # Parameters: shear_x, shear_y
        shear_x = float(params.get("shear_x", 0))
        shear_y = float(params.get("shear_y", 0))
        M = np.float32([[1, shear_x, 0], [shear_y, 1, 0]])
        output_image = cv2.warpAffine(input_image, M, (input_image.shape[1], input_image.shape[0]))
    
    elif transformation_type == "affine":
        # Parameters: src and dst as strings formatted like "x0,y0;x1,y1;x2,y2"
        src_points_str = params.get("src", "")
        dst_points_str = params.get("dst", "")
        if src_points_str and dst_points_str:
            src_pts = np.array([[float(n) for n in pt.split(',')] for pt in src_points_str.split(';')])
            dst_pts = np.array([[float(n) for n in pt.split(',')] for pt in dst_points_str.split(';')])
            M = cv2.getAffineTransform(src_pts, dst_pts)
            output_image = cv2.warpAffine(input_image, M, (input_image.shape[1], input_image.shape[0]))
    
    elif transformation_type == "perspective":
        # Parameters: src and dst as strings formatted like "x0,y0;x1,y1;x2,y2;x3,y3"
        src_points_str = params.get("src", "")
        dst_points_str = params.get("dst", "")
        if src_points_str and dst_points_str:
            src_pts = np.array([[float(n) for n in pt.split(',')] for pt in src_points_str.split(';')])
            dst_pts = np.array([[float(n) for n in pt.split(',')] for pt in dst_points_str.split(';')])
            M = cv2.getPerspectiveTransform(src_pts, dst_pts)
            output_image = cv2.warpPerspective(input_image, M, (input_image.shape[1], input_image.shape[0]))
    
    elif transformation_type == "resize":
        # Parameters: width, height
        width = int(params.get("width", input_image.shape[1]))
        height = int(params.get("height", input_image.shape[0]))
        output_image = cv2.resize(input_image, (width, height))
    
    elif transformation_type == "cropping":
        # Parameters: x, y, width, height
        x = int(params.get("x", 0))
        y = int(params.get("y", 0))
        width = int(params.get("width", input_image.shape[1]))
        height = int(params.get("height", input_image.shape[0]))
        output_image = input_image[y:y+height, x:x+width]
    
    return output_image

def generate_code(variable_name, input_variable, transformation_type, params):
    # Build a string representation for parameters in the generated cell.
    params_str = ", ".join([f'"{k}": {v}' for k, v in params.items()])
    code = f'''# Transformation Feature: {transformation_type.capitalize()}
params = {{{params_str}}}
{variable_name} = process_transformation({input_variable}, "{transformation_type}", params)
plt.figure(figsize=(6,6))
plt.imshow({variable_name})
plt.title("{transformation_type.capitalize()} Transformation")
plt.axis("off")
plt.show()
'''
    return code
