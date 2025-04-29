# build_init.py
# build_init.py
# buit_init.py
from euchre.utility import del_string
import os
import re
import sys
import ast

def build_init(directory, file_regex=r"[^_].*[.]py", class_regex=r"[^_].*"):
    filenames = list_files(directory, file_regex)
    to_import = get_class_names(directory, filenames, class_regex)

    sb = ""
    for filename in to_import.keys():
        if len(to_import[filename]) == 0: continue
        sb = sb + f"from .{filename[:-3]} import {del_string(to_import[filename])}\n"

    with open(os.path.join(directory, "__init__.py"), "w") as f:
        f.write(sb)
        f.write("__all__ = [\n")
        for filename in to_import.keys():
            if len(to_import[filename]) == 0: continue
            f.write("\t")
            imports = to_import[filename]
            f.write(del_string(imports, wrap="'"))
            f.write(",\n")
        f.write("]\n")

def list_files(directory, regex=r"[^_].*[.]py"):
    filenames = []
    for filename in sorted(os.listdir(directory)):
        if re.match(regex, filename):  # Only Bot_0.py, Bot_1.py, etc.
            filenames.append(filename)
    return filenames

def get_class_names(directory, filenames, regex):
    imports = {}

    for filename in filenames:
        fullpath = os.path.join(directory, filename)
        imports[filename] = []

        with open(fullpath, "r") as f:
            tree = ast.parse(f.read(), filename)

        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if not re.fullmatch(regex, node.name): continue
                imports[filename].append(node.name)
            # if not node.parent: continue
            if isinstance(node, ast.FunctionDef) and isinstance(node.parent, ast.Module):
                if not re.fullmatch(regex, node.name): continue
                imports[filename].append(node.name)                

    return imports

if __name__ == "__main__":
    if len(sys.argv) == 2:
        build_init(sys.argv[1])
    elif len(sys.argv) == 3:
        build_init(sys.argv[1], re.compile(sys.argv[2]))
    elif len(sys.argv) == 4:
        build_init(sys.argv[1], re.compile(sys.argv[2]), re.compile(sys.argv[3]))       
