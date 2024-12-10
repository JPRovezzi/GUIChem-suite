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
from modules.main_frame.functions import read_json
#------------------------------------------------------------
# Function definitions
def compile_c_script(
        c_script_path: str = None,
        c_script_name : str = None,
        output_path: str = None,
        output_name: str = None):
    '''Compile and run a C script.'''
    # If no path is provided, use the current directory
    if output_name is None:
        output_name = c_script_name
    if output_path is None:
        output_path = c_script_path

    # Check the operating system
    if os.name == 'nt':
        run_command = f"{output_path}{output_name}.exe"

        if not os.path.exists(run_command):
            # Compile the C script
            compile_command = " ".join((
                f"gcc {c_script_path}{c_script_name}.c", 
                f"-o {output_path}{output_name}.exe",
                "-lm"))
            subprocess.run(compile_command, shell=True, check=True)
    else:
        run_command = f"./{output_path}{output_name}"
        if not os.path.exists(run_command):
            # Compile the C script
            compile_command = "".join((
                f"gcc {c_script_path}{c_script_name}.c",
                f"-o {output_path}{output_name}",
                "-lm"))
            subprocess.run(compile_command, shell=True, check=True)
    # Run the compiled C script
    run_process = subprocess.run(run_command, shell=True, check=False)
    return run_process.stdout



def write_groups2picture(groups_dict):
    '''Write the molecule groups in the picture.'''
    
    module_location = os.path.dirname(os.path.abspath(__file__))
    
    pict_out = "/".join((
        read_json(
            path = module_location,
            filename = "tool",
            section = "FILENAME",
            key = "pict_out"),
        ))

    # Load the image
    image = Image.open(pict_out)

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
    image.save(pict_out)
    return None



def get_results(molecule_id,input_type):
    '''Get the molecule groups and save the SVG and PNG files.'''
    # Initialize the error and outcome variables
    outcome = (None,None)

    # Get the basic configs
    module_location = os.path.dirname(os.path.abspath(__file__))
    
    
    
    pict_in = "/".join((
        read_json(
            path = module_location,
            filename = "tool",
            section = "FILENAME",
            key = "pict_in"),
        ))
    
    svg2png_script = "/".join((
        read_json(
            path = module_location,
            filename = "tool",
            section = "FILENAME",
            key = "svg2png_script"),
        ))
    
    svg2png_exe = "/".join((
        read_json(
            path = module_location,
            filename = "tool",
            section = "FILENAME",
            key = "svg2png_exe"),
        ))
    
    path_script = "/".join((
        module_location,
        read_json(
            path = module_location,
            filename = "tool",
            section = "PATH",
            key = "svg2png_script"),
            
        ))
    
    path_exe = "/".join((
        module_location,
        read_json(
            path = module_location,
            filename = "tool",
            section = "PATH",
            key = "svg2png_exe"),
        )) 

    # Check if the molecule identifier is valid
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
        with open(pict_in, "w", encoding="utf-8") as file:
            file.write(svg_string)
        
        # Run the C script to convert the SVG to PNG
        compile_c_script(c_script_path = path_script, c_script_name = svg2png_script, output_name = svg2png_exe, output_path = path_exe)
        
        # Write the molecule groups in the picture
        write_groups2picture(molecule.unifac.subgroups)
        error = None
        outcome = (molecule, error)
        return outcome
    else:
        error = 2 # The identifier is empty
        outcome = (None,error)
        return outcome
    