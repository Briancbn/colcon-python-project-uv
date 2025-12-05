# Copyright 2025 Chen Bainian
# Licensed under the Apache License, Version 2.0

import os
import shutil

from colcon_core.environment_variable import EnvironmentVariable

"""Environment variable to override the UV executable"""
UV_COMMAND_ENVIRONMENT_VARIABLE = EnvironmentVariable(
    'UV_COMMAND', 'The full path to the uv executable')


def which_executable(environment_variable, executable_name):
    """
    Determine the path of an executable.

    An environment variable can be used to override the location instead of
    relying on searching the PATH.
    :param str environment_variable: The name of the environment variable
    :param str executable_name: The name of the executable
    :rtype: str
    """
    value = os.getenv(environment_variable)
    if value:
        return value
    return shutil.which(executable_name)


UV_EXECUTABLE = which_executable(
    UV_COMMAND_ENVIRONMENT_VARIABLE.name, 'uv')
