# step_manager.py

steps = [
    {
        "code": """import cv2
import numpy as np
import matplotlib.pyplot as plt
""",
        "desc": "Import Libraries",
        "type": "initial"
    }
]

def get_steps():
    return steps

def add_step(step):
    steps.append(step)

def update_step(idx, new_step):
    if 0 <= idx < len(steps):
        steps[idx] = new_step
