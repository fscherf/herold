import os

import yaml

from herold.utils.git import get_top_level

DEFAULT_CONFIG_ROOT = os.path.join(
    os.path.dirname(__file__),
    'default_config',
)


def get_config_from_repository():
    top_level = get_top_level()
    root = os.path.join(top_level, '.herold')
    path = os.path.join(root, 'config.yml')

    if not top_level:
        return root, None

    if not os.path.exists(path):
        return root, None

    return root, yaml.safe_load(open(path, 'r'))


def get_default_config():
    path = os.path.join(DEFAULT_CONFIG_ROOT, 'config.yml')

    return DEFAULT_CONFIG_ROOT, yaml.safe_load(open(path, 'r'))


def get_config():
    root, config = get_config_from_repository()

    if config:
        return root, config

    return get_default_config()
