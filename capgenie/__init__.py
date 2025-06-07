"""
CapGenie

A Python tool to programmatically edit CapCut project files via JSON manipulation.
"""

__version__ = "0.1.0"
__author__ = "Yanis Djeroro" # Or your preferred name
__email__ = "yanis.djeroro@gmail.com" # Or your preferred email

# Import main classes/functions for easy access
from .project_editor import Project
from .file_manager import CapCutFileManager # Assuming you want to expose this too

# Define what gets imported with "from capgenie import *"
__all__ = [
    "Project",
    "CapCutFileManager", # Add this if it's part of the public API
]
