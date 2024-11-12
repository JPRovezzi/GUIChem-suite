
# Importing required libraries

# Tkinter is a standard GUI library for Python.
import tkinter as tk

# The PIL library is used to work with images.
from PIL import ImageTk

def insert_image(where, image_path):
    '''Insert an image into a frame.'''
    image = ImageTk.PhotoImage(file=image_path)
    image_widget = tk.Label(
        where,
        image = image
        )
    image_widget.image = image
    image_widget.pack()
    return None

def place_image(where, posx, posy, image_path):
    '''Insert an image into a frame.'''
    image = ImageTk.PhotoImage(file=image_path)
    image_widget = tk.Label(
        where,
        image = image
        )
    image_widget.image = image
    image_widget.place(x=posx, y=posy, width=640, height=480)
    return None

def random_image(image_path):
    '''Return a random image from the image path.'''
    import os
    import random
    images = os.listdir(image_path)
    print(images)
    image = random.choice(images)
    image = image_path + "/" + image
    return image