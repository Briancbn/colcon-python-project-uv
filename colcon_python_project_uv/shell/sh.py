from pathlib import Path
from colcon_core.shell import logger
from colcon_core.shell.template import expand_template

def create_activate_script(prefix_path, venv_path, python_lib_path):
    activate_script_path = prefix_path / 'activate.sh'
    logger.info("Creating activate script '%s'" % activate_script_path)
    expand_template(
        Path(__file__).parent / 'template' / 'activate.sh.em',
        activate_script_path,
        {
            'venv_path': venv_path,
            'python_lib_path': python_lib_path,
        })
    return activate_script_path
