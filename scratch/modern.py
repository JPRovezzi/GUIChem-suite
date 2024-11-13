import customtkinter as ctk
from PIL import Image
import random

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

def random_image(image_path):
    '''Return a random image from the image path.'''
    import os
    import random
    images = os.listdir(image_path)
    image = random.choice(images)
    image = image_path + "/" + image
    return image

def change_appearance_mode_event(new_appearance_mode: str):
    ctk.set_appearance_mode(new_appearance_mode)
    #place_image(frame, 0, 0, "assets/backgrounds")
    light_image=Image.open(random_image("assets/backgrounds/light")).rotate(random.choice([0,90,180,270]))
    dark_image=Image.open(random_image("assets/backgrounds/dark")).rotate(random.choice([0,90,180,270]))
    image = ctk.CTkImage(light_image=light_image, dark_image=dark_image,size=(640,640))
    image_widget.configure(image=image)
    appearance_menu.set("CTk Option Menu")
    if new_appearance_mode == "Light":
        ctk.set_default_color_theme("blue")
    else:
        ctk.set_default_color_theme("dark-blue")


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.resizable(0, 0)  # Disable resizing

root.geometry("640x480")


frame = ctk.CTkFrame(master=root)
menuframe = ctk.CTkFrame(master=root)
#menuframe.grid(row=0, pady=10, padx=0,sticky="nw")
file_menu = ctk.CTkOptionMenu(menuframe,corner_radius=0, values=["New", "Open", "Save", "Exit"])
file_menu.grid(row=0, column=0, pady=10, padx=10)
file_menu.set("File")
appearance_menu = ctk.CTkOptionMenu(menuframe,corner_radius=0, values=["Light", "Dark", "System"], command=change_appearance_mode_event)
appearance_menu.grid(row=0, column=1, pady=10, padx=10)
appearance_menu.set("Color")
menuframe.pack(anchor="w",fill="both",padx=0, pady=0)
place_image(frame, 0, 0, "assets/backgrounds")



subframe = ctk.CTkFrame(master=frame,corner_radius=90)

ctk.CTkLabel(master=subframe, text="Username",font=("ArialBlack",18)).pack(pady=10)
ctk.CTkLabel(master=subframe, text="Username",font=("ArialBlack",18)).pack(pady=10)
ctk.CTkLabel(master=subframe, text="Username",font=("ArialBlack",18)).pack(pady=10)
ctk.CTkLabel(master=subframe, text="Username",font=("ArialBlack",18)).pack(pady=10)
subframe.pack(pady=100)
frame.pack(fill="both", expand=True, padx=0, pady=0)





root.mainloop()