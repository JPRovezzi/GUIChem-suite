'''This module contains functions to handle images in the GUI.'''

# Importing required libraries:
# Os is a standard library for Python that provides functions to interact with
import os
# Random is a standard library for Python that provides functions to generate
# random numbers.
import random
# Tkinter is a standard GUI library for Python.
import tkinter as tk
# CustomTkinter is a custom GUI library for Python.
import customtkinter as ctk
# The PIL library is used to work with images.
from PIL import ImageTk, Image
# frameRoot is the main frame of the GUIChem-suite application
import modules.guiFrames.frame_root as frame_root
#------------------------------------------------------------
def insert_image(where, image_path):
    '''Insert an image into a frame.'''
    image = ImageTk.PhotoImage(file=image_path)
    picture = tk.Label(
        where,
        image = image
        )
    picture.image = image
    picture.pack()
    return None

def random_image(image_path):
    '''Return a random image from the image path.'''
    images = os.listdir(image_path)
    image = random.choice(images)
    image = image_path + "/" + image
    return image

def place_image(where, posx, posy, image_path):
    '''Insert an image into a frame.'''
    light_image=Image.open(random_image(image_path+"/light")).rotate(random.choice([0,90,180,270]))
    dark_image=Image.open(random_image(image_path+"/dark")).rotate(random.choice([0,90,180,270]))
    image = ctk.CTkImage(light_image=light_image, dark_image=dark_image,size=(640,640))
    image_widget = ctk.CTkLabel(
        where,
        image = image, text=None
        )
    image_widget.image = image
    image_widget.place(x=posx, y=posy)
    light_image.close()
    dark_image.close()
    return None

def change_appearance_mode_event(new_appearance_mode: str):
    '''Change the appearance mode of the GUI.'''
    # Reset the appearance menu label
    frame_root.appearance_menu.set("Theme")
    # Change the appearance mode
    ctk.set_appearance_mode(new_appearance_mode)
        # Change the default color theme
    if new_appearance_mode == "Light":
        ctk.set_default_color_theme("blue")
    else:
        ctk.set_default_color_theme("dark-blue")
    # Change light and dark mode images
    light_image=Image.open(
        random_image("assets/backgrounds/light")
        ).rotate(random.choice([0,90,180,270]))
    dark_image=Image.open(
        random_image("assets/backgrounds/dark")
        ).rotate(random.choice([0,90,180,270]))
    image = ctk.CTkImage(
        light_image=light_image,
        dark_image=dark_image,
        size=(640,640))
    # Change the image of the main frame
    frame_root.root.winfo_children()[0].configure(image=image)
    return None
