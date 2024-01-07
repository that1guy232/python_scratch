import ast


def extract_classes_from_file(filename):
    """Extracts classes from a Python file using the AST module."""
    with open(filename, 'r') as f:
        node = ast.parse(f.read())

    return [n for n in node.body if isinstance(n, ast.ClassDef)]


def write_class_to_file(class_node, directory="."):
    """Writes a single class to its own Python file."""
    class_name = class_node.name
    code = ast.unparse(class_node)  # Convert AST node back to source code
    with open(f"{directory}/{class_name}.py", 'w') as f:
        f.write(code)


def split_classes_to_files(filename, directory="."):
    """Splits classes in a Python file into individual files."""
    classes = extract_classes_from_file(filename)
    for class_node in classes:
        write_class_to_file(class_node, directory)


if __name__ == "__main__":
    input_filename = "main.py"
    output_directory = "."  # Current directory, change if needed
    split_classes_to_files(input_filename, output_directory)
