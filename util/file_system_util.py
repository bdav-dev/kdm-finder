import os

def get_absolute_path(py_file_location: str, *relative_path: str) -> str:
    dirname = os.path.dirname(os.path.abspath(py_file_location))
    return os.path.join(dirname, os.path.join(*relative_path))
