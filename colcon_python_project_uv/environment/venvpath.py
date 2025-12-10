# Copyright 2025 Chen Bainian
# Licensed under the Apache License, Version 2.0

from pathlib import Path

from colcon_core import shell
from colcon_core.environment import EnvironmentExtensionPoint
from colcon_core.environment import logger
from colcon_core.plugin_system import satisfies_version
from colcon_core.python_install_path import get_python_install_path
from colcon_python_project_uv.venv.location import get_venv_path


class VenvPathEnvironment(EnvironmentExtensionPoint):
    """Extend the `PYTHONPATH` variable to find VENV modules."""

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(
            EnvironmentExtensionPoint.EXTENSION_POINT_VERSION, '^1.0')

    def create_environment_hooks(self, prefix_path, pkg_name):  # noqa: D102
        hooks = []

        # Quick hack to get the install root path
        base_install_path = Path(prefix_path)
        if base_install_path.name == pkg_name:
            base_install_path = base_install_path.parent

        venv_path = base_install_path / get_venv_path()
        venv_python_path = get_python_install_path('purelib', {'base': venv_path})
        if not venv_python_path.exists():
            return hooks

        # Check if this is a python package
        python_path = get_python_install_path('purelib', {'base': prefix_path})
        logger.log(1, "checking '%s'" % python_path)
        if python_path.exists():
            hooks += shell.create_environment_hook(
                'venvpath', prefix_path, pkg_name,
                'PYTHONPATH', str(venv_python_path.absolute()), mode='prepend')

        # platlib_path = get_python_install_path(
        #     'platlib', {'base': prefix_path, 'platbase': prefix_path})
        # if python_path != platlib_path:
        #     logger.log(1, "checking '%s'" % platlib_path)
        #     if platlib_path.exists():
        #         rel_platlib_path = platlib_path.relative_to(prefix_path)
        #         hooks += shell.create_environment_hook(
        #             'pythonpath', prefix_path, pkg_name,
        #             'PYTHONPATH', str(rel_platlib_path), mode='prepend')

        return hooks
