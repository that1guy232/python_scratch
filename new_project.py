import os
import shutil
import sys

def copy_and_rename(src_dir, dest_name):
    dest_dir = os.path.join(os.path.dirname(src_dir), dest_name)
    shutil.copytree(src_dir, dest_dir)
    print(f'Copied {src_dir} to {dest_name}')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python new_project.py [new_project_name]")
        sys.exit(1)
        
    new_project_name = sys.argv[1]
    current_dir = os.path.dirname(os.path.abspath(__file__))
    empty_project_path = os.path.join(current_dir, 'empty_project')
    
    if not os.path.exists(empty_project_path):
        print(f"Source directory {empty_project_path} does not exist.")
        sys.exit(1)
        
    copy_and_rename(empty_project_path, new_project_name)