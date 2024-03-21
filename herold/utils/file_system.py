import logging
import shutil
import os

logger = logging.getLogger('herold.file-system')


def iter_directory(root_dir):
    for root, _, files in os.walk(root_dir):
        for file in files:
            abs_path = os.path.join(root, file)
            rel_path = os.path.relpath(abs_path, root_dir)

            yield abs_path, rel_path


def make_directories(path):
    abs_path = os.path.abspath(path)

    if os.path.exists(abs_path):
        return

    logger.debug('making directories %s', abs_path)

    os.makedirs(abs_path)


def copy_files(source, destination):
    destination_dirname = os.path.dirname(destination)

    logger.debug('copying %s to %s', source, destination)

    if not os.path.exists(destination_dirname):
        os.makedirs(destination_dirname)

    shutil.copy(src=source, dst=destination)
