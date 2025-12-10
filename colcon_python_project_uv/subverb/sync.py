# Copyright 2025 Chen Bainian
# Licensed under the Apache License, Version 2.0

from colcon_core.package_discovery import add_package_discovery_arguments
from colcon_core.plugin_system import satisfies_version
from colcon_python_project_uv.subverb import VenvSubverbExtensionPoint
from colcon_python_project_uv.venv.api import sync_uv_venv


class SyncVenvSubverb(VenvSubverbExtensionPoint):
    """Synchronize venv dependencies."""

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(
            VenvSubverbExtensionPoint.EXTENSION_POINT_VERSION, '^1.0')

    def add_arguments(self, *, parser):  # noqa: D102
        add_package_discovery_arguments(parser)

        # only added so that package selection arguments can be used
        # which use the install directory to store .venv information
        parser.add_argument(
            '--install-base',
            default='install',
            help='The base path for all install directories (default: install)')

    def main(self, *, context):  # noqa: D102
        args = context.args
        sync_uv_venv(args)
