
# Importing required libraries

# Tkinter is a standard GUI library for Python.
import tkinter as tk
import customtkinter as ctk
import random

# The PIL library is used to work with images.
from PIL import ImageTk, Image

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

def place_image_old(where, posx, posy, image_path):
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
    image = random.choice(images)
    image = image_path + "/" + image
    return image

def place_image(where, posx, posy, image_path):
    '''Insert an image into a frame.'''
    global image_widget
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
    import modules.guiFrames.frameRoot as frameRoot
    ctk.set_appearance_mode(new_appearance_mode)
    #place_image(frame, 0, 0, "assets/backgrounds")
    light_image=Image.open(random_image("assets/backgrounds/light")).rotate(random.choice([0,90,180,270]))
    dark_image=Image.open(random_image("assets/backgrounds/dark")).rotate(random.choice([0,90,180,270]))
    image = ctk.CTkImage(light_image=light_image, dark_image=dark_image,size=(640,640))
    image_widget.configure(image=image)
    frameRoot.appearance_menu.set("CTk Option Menu")
    if new_appearance_mode == "Light":
        ctk.set_default_color_theme("blue")
    else:
        ctk.set_default_color_theme("dark-blue")