''' This module is used to handle the SVG files. It contains the functions to
convert the SVG to PNG and write the molecule groups in the picture. '''
#------------------------------------------------------------
# Import the required libraries
# The subprocess library is used to run external commands.
import subprocess
# The os library provides a way to interact with the operating system.
import os
# The PIL library is used to work with images.
from PIL import Image, ImageDraw, ImageFont
# UgroPy is a Python library that provides a simple interface to the UNIFAC
# group contribution method.
from ugropy import Groups
from ugropy import unifac
#------------------------------------------------------------
# Function definitions
def run_c_script(c_script_path: str, output_path: str):
    '''Compile and run a C script.'''
    if os.name == 'nt':
        run_command = f"{output_path}.exe"
        if not os.path.exists("SvgToPng.exe"):
            # Compile the C script
            compile_command = f"gcc {c_script_path} -o {output_path}"
            subprocess.run(compile_command, shell=True, check=True)
    else:
        run_command = f"./{output_path}"
        if not os.path.exists("SvgToPng"):
            # Compile the C script
            compile_command = f"gcc {c_script_path} -o {output_path} -lm"
            subprocess.run(compile_command, shell=True, check=True)
    # Run the compiled C script
    run_process = subprocess.run(run_command, shell=True, check=False)
    return run_process.stdout

def write_groups2picture(groups_dict):
    '''Write the molecule groups in the picture.'''
    # Load the image
    image = Image.open('output.png')

    # Initialize ImageDraw
    draw = ImageDraw.Draw(image)

    # Define the text and position
    #text = list(groups_dict.keys())[0]
    position = (25, 10)

    # Load a font
    font = ImageFont.load_default()

    # Add text to image
    for i, key in enumerate(groups_dict.keys()):
        position = (25, 10 + i * 25)  # Adjust the position for each key
        draw.text(position, key, font=font, fill=(0, 0, 0))

    # Save the image
    image.save('output.png')
    return None

def get_results(molecule_id,input_type):
    '''Get the molecule groups and save the SVG and PNG files.'''
    outcome = (None,None)
    if molecule_id is not None and molecule_id != "":
        try:
            molecule = Groups(
                identifier = molecule_id,
                identifier_type = input_type
                )
            molecule_groups = unifac.get_groups(
                identifier = molecule_id,
                identifier_type = input_type
                )
        except (IndexError,TypeError):
            error = 1 # The identifier is not valid
            outcome = (None, error)
            return outcome
        # Get the SVG information
        svg_string = molecule_groups.get_solution_svg()
        # Save the SVG
        with open("input.svg", "w", encoding="utf-8") as file:
            file.write(svg_string)
        # Run the C script to convert the SVG to PNG
        run_c_script("SvgToPng.c", "SvgToPng")
        # Write the molecule groups in the picture
        write_groups2picture(molecule.unifac.subgroups)
        error = None
        outcome = (molecule, error)
        return outcome
    else:
        error = 2 # The identifier is empty
        outcome = (None,error)
        return outcome
    