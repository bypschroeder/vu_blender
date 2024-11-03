import sys
import os

def add_subdirs_to_sys_path(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if os.path.basename(dirpath) == "__pycache__":
            continue  
        sys.path.append(dirpath)

def get_relative_path(relative_path):
    project_base_dir = os.path.dirname(os.path.abspath(__file__)) 
    project_base_dir = os.path.abspath(os.path.join(project_base_dir, "..")) 

    return os.path.join(project_base_dir, *relative_path.split('/'))