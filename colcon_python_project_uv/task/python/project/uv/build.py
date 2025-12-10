# Copyright 2025 Chen Bainian
# Licensed under the Apache License, Version 2.0

import logging
import os.path
import re
from pathlib import Path
from subprocess import PIPE

from colcon_core.environment import create_environment_hooks
from colcon_core.environment import create_environment_scripts
from colcon_core.logging import colcon_logger
from colcon_core.plugin_system import satisfies_version
from colcon_core.shell import get_command_environment
from colcon_core.task import run
from colcon_core.task import TaskExtensionPoint
from colcon_python_project_uv.task.python.project.uv import UV_EXECUTABLE
from colcon_python_project.wheel import install_wheel

logger = colcon_logger.getChild(__name__)

def _get_wheel_path(uv_build_stderr):
    uv_build_out = uv_build_stderr.decode('utf-8')
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    uv_build_plain = ansi_escape.sub('', uv_build_out)
    word = "Successfully built "
    return uv_build_plain[
        uv_build_plain.find(word) + len(word):-1]


class UVBuildTask(TaskExtensionPoint):
    """Build Python project packages."""

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(TaskExtensionPoint.EXTENSION_POINT_VERSION, '^1.0')

        # avoid debug message from asyncio when colcon uses debug log level
        asyncio_logger = logging.getLogger('asyncio')
        asyncio_logger.setLevel(logging.INFO)

        distutils_logger = logging.getLogger('distlib.util')
        distutils_logger.setLevel(logging.WARN)

    async def build(self, *, additional_hooks=None):  # noqa: D102
        pkg = self.context.pkg
        args = self.context.args

        logger.info(f"Building UV project in '{args.path}'")

        env = await get_command_environment(
            'python_project_uv', args.build_base, self.context.dependencies)

        self.progress('prepare')

        wheel_directory = Path(args.build_base) / 'wheel'
        wheel_directory.mkdir(parents=True, exist_ok=True)

        if UV_EXECUTABLE is None:
            raise RuntimeError("Could not find 'uv' executable")

        cmd = [
            UV_EXECUTABLE,
            'build',
            '--wheel',
            '--package', pkg.name,
            '--out-dir', str(wheel_directory),
        ]

        self.progress('build')
        rc = await run(
            self.context, cmd, cwd=pkg.path, env=env, capture_output=True)
        if rc and rc.returncode:
            return rc.returncode

        if rc.stderr is None:
            raise RuntimeError(
                "Failed to capture stderr from 'uv build'"
            )

        self.progress('install')
        wheel_path = Path(_get_wheel_path(rc.stderr))
        dist_info_dir = install_wheel(
            wheel_path, args.install_base)

        libdir = dist_info_dir.parent
        records = []

        hooks = create_environment_hooks(args.install_base, pkg.name)
        records += [
            (Path(os.path.relpath(hook, libdir)).as_posix(), '', '')
            for hook in hooks
        ]

        scripts = create_environment_scripts(
            pkg, args, default_hooks=hooks, additional_hooks=additional_hooks)
        records += [
            (Path(os.path.relpath(script, libdir)).as_posix(), '', '')
            for script in scripts
        ]

        with (dist_info_dir / 'RECORD').open('a') as f:
            f.writelines(','.join(rec) + '\n' for rec in records)


    def _stdout_callback(self, line):
        self.context.put_event_into_queue(StdoutLine(line))

    def _stderr_callback(self, line):
        self.context.put_event_into_queue(StderrLine(line))
