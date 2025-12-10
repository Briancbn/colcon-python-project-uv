import os
from pathlib import Path

_uv_venv_project_path = '.uv_python_project_venv'
_uv_venv_project_venv_subdirectory = '.venv'

def get_venv_path():
    return get_uv_venv_path() / _uv_venv_project_venv_subdirectory


def get_uv_venv_path():
    """
    Get the base path for the uv project maintaining .venv.
    """
    path = None
    path = Path(_uv_venv_project_path)

    if path == os.devnull:
        return None

    return Path(str(path))

def create_uv_venv_path(install_base):
    path = Path(str(install_base)) / get_uv_venv_path()
    try:
        os.makedirs(str(path))
    except FileExistsError:
        pass  # Do nothing

    print(f"Using UV venv path '{path}'")
