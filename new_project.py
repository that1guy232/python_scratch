import os
import shutil
import sys


def copy_and_rename(src_dir, dest_name):
    dest_dir = os.path.join(os.path.dirname(src_dir), dest_name)
    shutil.copytree(src_dir, dest_dir)
    print(f'Copied {src_dir} to {dest_name}')
    return dest_dir


def create_settings_file(dir_path, project_name):
    settings_content = f"""
TITLE = '{project_name}'
SCREEN_SCALE = 64
SCREEN_WIDTH = 16 * SCREEN_SCALE  # 16 * 64 = 1024
SCREEN_HEIGHT = 9 * SCREEN_SCALE  # 9 * 64 = 576
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FPS = 90

"""
    with open(os.path.join(dir_path, 'settings.py'), 'w') as settings_file:
        settings_file.write(settings_content)


def create_project(project_name):
    print(f"Creating new project {project_name}")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    empty_project_path = os.path.join(current_dir, 'empty_project')
    if not os.path.exists(empty_project_path):
        print(f"Source directory {empty_project_path} does not exist.")
        sys.exit(1)

    new_dir = copy_and_rename(empty_project_path, project_name)
    create_settings_file(new_dir, project_name)


    pass

def main():
    if len(sys.argv) != 2:
        print("Usage: python new_project.py [new_project_name]")
        sys.exit(1)

    new_project_name = sys.argv[1]
    current_dir = os.path.dirname(os.path.abspath(__file__))

    empty_project_path = os.path.join(current_dir, 'empty_project')

    if not os.path.exists(empty_project_path):
        print(f"Source directory {empty_project_path} does not exist.")
        sys.exit(1)

    new_dir = copy_and_rename(empty_project_path, new_project_name)
    create_settings_file(new_dir, new_project_name)


if __name__ == "__main__":
    main()
