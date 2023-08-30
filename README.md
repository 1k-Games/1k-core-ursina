# 1k-core-ursina (core1k)
Core library for Ursina engine

This code base is used to import core/common game systems that can be used as the base for any desired genre that is choosen

pip uninstall 1k-core-ursina
pip install --upgrade --no-cache-dir git+https://github.com/1k-Games/1k-core-ursina.git@[branch]
# Game Manager
The "game_manager" class can be used for managing game state and other game entities, scenes, menus, etc.

# Network Manager

# Process Manager
Support for handing off processes to non-primary cores are available in the Process Manager.

### TODO:
* Determine the hardware cores and how many to allow for additional processing. 
* Send/Receive requests 

# ______________Controller(?)
Each controller can be the base class for the player controller

# Create Executable:
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {

    "packages": ["ursina"], # Include Ursina package
    "excludes": [], # Add packages you want to exclude
    "include_files": ["assets/"] # Add files you want to include
}

#base="Win32GUI" should be used only for Windows GUI app

#base = "Win32GUI" if sys.platform == "win32" else None

setup(
    
    name="TheEnd_Invasion",
    version="0.1",
    description="The End: Invasion",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", target_name='TheEnd_Invasion', base=base)], # Replace main.py with your main script
)