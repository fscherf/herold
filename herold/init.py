import os

from herold.config import DEFAULT_CONFIG_ROOT
from herold.utils.git import get_top_level

from herold.utils.file_system import (
    make_directories,
    iter_directory,
    copy_files,
)


def init(cli_args, config_root, config):
    top_level = get_top_level()

    if not top_level:
        raise RuntimeError('not in a git repository')

    repo_config_root = os.path.join(top_level, '.herold')

    make_directories(repo_config_root)

    for abs_path, _ in iter_directory(DEFAULT_CONFIG_ROOT):
        copy_files(abs_path, repo_config_root)
