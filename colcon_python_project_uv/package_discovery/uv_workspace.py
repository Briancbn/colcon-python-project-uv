# Copyright 2025 Chen Bainian
# Licensed under the Apache License, Version 2.0

from colcon_uv.package_identification.uv import UVPackageIdentification
from colcon_core.package_discovery import PackageDiscoveryExtensionPoint
from colcon_core.package_identification import identify
from colcon_core.package_identification import IgnoreLocationException
from colcon_core.plugin_system import satisfies_version


class UVWorkspacePackageDiscovery(PackageDiscoveryExtensionPoint):
    """Discover packages which are part of a uv workspace."""

    # the priority should be very low because we need to discover the
    # workspaces themselves before we can enumerate their sub-packages
    PRIORITY = 10

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(
            PackageDiscoveryExtensionPoint.EXTENSION_POINT_VERSION,
            '^1.1')

    def has_parameters(self, *, args):  # noqa: D102
        return None

    def discover(self, *, args, identification_extensions):  # noqa: D102
        # Nested workspaces are not currently supported by uv. If they ever
        # are, this code should be updated to run the whole process again until
        # no additional member package paths are found.

        paths = set()
        for extensions_same_prio in identification_extensions.values():
            for extension in extensions_same_prio.values():
                if isinstance(extension, UVPackageIdentification):
                    paths.update(extension.workspace_package_paths)
                    extension.workspace_package_paths.clear()

        descs = set()
        for path in paths:
            try:
                result = identify(identification_extensions, path)
            except IgnoreLocationException:
                continue
            if result:
                descs.add(result)
        return descs
