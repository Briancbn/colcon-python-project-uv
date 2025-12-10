# Copyright 2025 Chen Bainian
# Licensed under the Apache License, Version 2.0

from colcon_core.package_identification import logger
from colcon_core.package_identification \
    import PackageIdentificationExtensionPoint
from colcon_core.plugin_system import satisfies_version
from colcon_python_project.spec import load_and_cache_spec
from colcon_python_project.spec import SPEC_NAME


class UVPackageIdentification(PackageIdentificationExtensionPoint):
    """Identify Python packages with `pyproject.toml` metadata and uv build."""

    # the priority should be higher than python-project
    PRIORITY = 160

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
        uv = spec.get('tool', {}).get('uv')
        build_backend = spec.get('build-system', {}).get('build-backend')
        if not name:
            return

        is_python_uv = (uv or build_backend == 'uv_build')
        if not is_python_uv:
            return

        if desc.name is not None and desc.name != name:
            msg = 'Package name already set to different value'
            logger.error(msg)
            raise RuntimeError(msg)
        desc.name = name
        desc.type = 'python.project.uv'
