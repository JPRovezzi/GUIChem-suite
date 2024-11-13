''' This module is used to handle the SVG files. It contains the functions to convert the SVG to PNG and write the molecule groups in the picture. ''' 


# Import the required libraries
# UgroPy is a Python library that provides a simple interface to the UNIFAC group contribution method.
from ugropy import Groups
from ugropy import unifac
# The subprocess library is used to run external commands.
import subprocess
# The os library provides a way to interact with the operating system.
import os
# The PIL library is used to work with images.
from PIL import Image, ImageDraw, ImageFont

#------------------------------------------------------------
# Function definitions
def run_c_script(c_script_path: str, output_path: str):
    '''Compile and run a C script.'''
    if not os.path.exists("SvgToPng.exe"):  
        # Compile the C script
        compile_command = f"gcc {c_script_path} -o {output_path}"
        compile_process = subprocess.run(compile_command, shell=True, check=True)
    # Run the compiled C script
    run_command = f"./{output_path}"
    #run_process = subprocess.run(run_command, shell=True, check=True, capture_output=True, text=True)
    run_process = subprocess.run(run_command)
    return run_process.stdout

def write_groups2picture(dict):
    '''Write the molecule groups in the picture.'''
    # Load the image
    image = Image.open('output.png')
    #print("picture loaded")
    # Initialize ImageDraw
    draw = ImageDraw.Draw(image)

    # Define the text and position
    #text = list(dict.keys())[0]
    position = (25, 10)

    # Load a font
    font = ImageFont.load_default()

    # Add text to image
    for i, key in enumerate(dict.keys()):
        position = (25, 10 + i * 25)  # Adjust the position for each key
        draw.text(position, key, font=font, fill=(0, 0, 0))
    #draw.text(position, text, font=font, fill=(0, 0, 0))

    # Save the image
    image.save('output.png')
    return None

def get_results(molecule_id,input_type):  
    outcome = (None,None)
    if molecule_id != None and molecule_id != "":
            try:
                #print(input_type, molecule_id)
                molecule = Groups(
                    identifier = molecule_id,
                    identifier_type = input_type
                    )
                molecule_groups = unifac.get_groups(
                    identifier = molecule_id,
                    identifier_type = input_type
                    )
            except:
                error = 1
                #print(1)
                outcome = (None, error)
                return outcome
            svg_string = molecule_groups.get_solution_svg() # Get the SVG information
            with open("input.svg", "w") as file:
                file.write(svg_string) #Save the SVG
            run_c_script("SvgToPng.c", "SvgToPng") # Run the C script to convert the SVG to PNG
            write_groups2picture(molecule.unifac.subgroups) # Write the molecule groups in the picture
            #print("The molecule groups are displayed below.")
            error = None
            #print(0)
            outcome = (molecule, error)
            return outcome
    else:
        error = 2
        #print(2)
        outcome = (None,error)
        return outcome