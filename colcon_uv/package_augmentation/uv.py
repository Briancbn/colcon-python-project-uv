# Copyright 2025 Chen Bainian
# Licensed under the Apache License, Version 2.0

import logging

from colcon_core.plugin_system import satisfies_version
from colcon_core.package_augmentation.python import \
    create_dependency_descriptor
from colcon_python_project.package_augmentation.pep621 \
    import PEP621PackageAugmentation
from colcon_python_project.spec import load_and_cache_spec


class UVPackageAugmentation(PEP621PackageAugmentation):
    """Augment UV Python packages."""

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(
            PEP621PackageAugmentation.EXTENSION_POINT_VERSION,
            '^1.0')

        # avoid debug message from asyncio when colcon uses debug log level
        asyncio_logger = logging.getLogger('asyncio')
        asyncio_logger.setLevel(logging.INFO)

    def augment_package(  # noqa: D102
        self, desc, *, additional_argument_names=None
    ):
        if desc.type != 'python.uv':
            return

        desc.type = 'python.project'
        super().augment_package(
            desc,
            additional_argument_names=additional_argument_names
        )

        # load test dependency from dependency group
        spec = load_and_cache_spec(desc)
        dependency_groups = spec.get('dependency-groups', {})
        desc.dependencies['test'].update(
            create_dependency_descriptor(d)
            for d in dependency_groups.get('test') or ())
        desc.type = 'python.uv'
