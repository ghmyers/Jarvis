"""
TITLE: helper_functions.py
AUTHOR: Harrison Myers
DATE: 2025-04-27
DESCRIPTION: Utility functions for the Jarvis module
"""

#!/usr/bin/env python3
import os
import sys

# Get project directory dynamically
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(PROJECT_DIR)

# Ensure PROJECT_DIR is in sys.path for imports
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

# Append src/ to Python's module search path
sys.path.append(os.path.join(PROJECT_DIR, "src"))

from zipfile import ZipFile
import pandas as pd

def create_dirs():
    """
    Unzips the external-data folder and creates the directories necessary to run the 
    rest of the script. Changes the working directory, and returns the working
    directory path, and the path of the enclosing, unzipped "data" folder
    containing the datafiles. 
    """
    # Create relative directory path and change directory
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)
    
    # Make data folder and unzip reports to this folder
    try:
        os.mkdir("data")
        # loading the temp.zip and creating a zip object 
        with ZipFile(dir_path + "\\external-data.zip") as zObject: 
            # Extracting all the members of the zip into data
            zObject.extractall(dir_path)
    except:
        pass
    
    # Make a path that points to the reports folder where data is stored
    data_dir = dir_path + "\\data"
    
    return dir_path, data_dir

dir_path, data_dir = create_dirs()

def load_model_results(filename):
    """
    Reads model results from a .txt file and saves the text and labels as a dataframe
    """
    texts     = []
    labels    = []
    NB_class  = []
    SGD_class = []
    with open(filename, 'r') as file:   # Open the desired file
        lines = []                      # Create an empty list for storing lines in the file
        for line in file:               # Loop through every line in the file
            lines.append(line)          # Append each line to the list, lines

        for line in lines:              # Loop through every line in lines
            try:
                str_list = line.split(",")  # try to split the lines by ,
                texts.append(str_list[0])
                labels.append(str_list[1].strip(" "))
                NB_class.append(int(str_list[2]))
                SGD_class.append(int(str_list[3]))
            except:                         
                pass
            
    # turn into dataframe
    data = {"Text": texts, 
            "Label": labels, 
            "NB_class": NB_class, 
            "SGD_class":SGD_class}
    df = pd.DataFrame(data)
    
    return df
