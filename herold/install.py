import os

from herold.utils.file_system import make_directories, iter_directory, copy_files
from herold.utils.git import get_top_level

HOOKS_ROOT = os.path.join(os.path.dirname(__file__), 'hooks')


def install(cli_args, config_root, config):
    top_level = get_top_level()

    if not top_level:
        raise RuntimeError('not in a git repository')

    git_hooks_root = os.path.join(top_level, '.git/hooks')

    make_directories(git_hooks_root)

    for abs_path, _ in iter_directory(HOOKS_ROOT):
        copy_files(abs_path, git_hooks_root)
