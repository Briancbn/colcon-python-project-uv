# Copyright 2025 Chen Bainian
# Licensed under the Apache License, Version 2.0

from colcon_core.package_identification import logger
from colcon_core.package_identification \
    import PackageIdentificationExtensionPoint
from colcon_python_project.spec import load_and_cache_spec
from colcon_python_project.spec import SPEC_NAME
from colcon_core.plugin_system import satisfies_version


class UVWorkspaceIdentification(PackageIdentificationExtensionPoint):
    """
    Identify UV workspaces with `pyproject.toml` files.

    This extension does not actually identify any packages per se, but is a
    necessary component for CargoWorkspacePackageDiscovery to function.
    """

    # Higher than package identification
    PRIORITY = 170

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(
            PackageIdentificationExtensionPoint.EXTENSION_POINT_VERSION,
            '^1.0')
        self.workspace_package_paths = set()

    def identify(self, desc):  # noqa: D102
        if desc.type is not None and desc.type != 'python.project.uv':
            return

        spec_file = desc.path / SPEC_NAME
        if not spec_file.is_file():
            return

        spec = load_and_cache_spec(desc)
        name = spec.get('project', {}).get('name')
        workspace = spec.get('tool', {}).get('uv', {}).get('workspace')
        if not name:
            return

        if desc.name is not None and desc.name != name:
            msg = 'Package name already set to different value'
            logger.error(msg)
            raise RuntimeError(msg)

        if workspace is None:
            return

        logger.info("colcon workspace!!")

        ws_members = {
            member
            for pattern in workspace.get('members', ())
            for member in desc.path.glob(pattern)
        }

        ws_members.difference_update(
            exclude
            for pattern in workspace.get('exclude', ())
            for exclude in desc.path.glob(pattern)
        )
        self.workspace_package_paths.update(ws_members)

        workspace_metadata = workspace.get('metadata', {})
        colcon_metadata = workspace_metadata.get('colcon', {})
        self.workspace_package_paths.update(
            member
            for pattern in colcon_metadata.get('additional-packages', ())
            for member in desc.path.glob(pattern)
        )
        logger.info(f"workspace paths: {self.workspace_package_paths}")
