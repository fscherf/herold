import argparse

import simple_logging_setup

from herold.patch_commit_message import patch_commit_message
from herold.changelog import changelog
from herold.releases import releases
from herold.config import get_config
from herold.install import install
from herold.version import version
from herold.check import check
from herold.find import find
from herold.init import init

COMMANDS = {
    'patch-commit-message': patch_commit_message,
    'changelog': changelog,
    'releases': releases,
    'version': version,
    'install': install,
    'check': check,
    'find': find,
    'init': init,
}


def add_common_args(parser):
    parser.add_argument(
        '-l',
        '--log-level',
        choices=['debug', 'info', 'warn', 'error', 'critical'],
        default='info',
    )

    parser.add_argument(
        '--loggers',
        type=str,
        nargs='+',
    )

    parser.add_argument(
        '--traceback',
        action='store_true',
    )


def parse_command_line_args(argv):
    parser = argparse.ArgumentParser(prog='herold')

    sub_parser = parser.add_subparsers(
        dest='command',
        required=True,
    )

    # version #################################################################
    version_parser = sub_parser.add_parser('version')

    add_common_args(version_parser)

    # init ####################################################################
    init_parser = sub_parser.add_parser('init')

    add_common_args(init_parser)

    # install #################################################################
    install_parser = sub_parser.add_parser('install')

    add_common_args(install_parser)

    # patch-commit-message ####################################################
    patch_commit_message_parser = sub_parser.add_parser('patch-commit-message')

    add_common_args(patch_commit_message_parser)

    patch_commit_message_parser.add_argument('--commit-message-file')
    patch_commit_message_parser.add_argument('--commit-source')
    patch_commit_message_parser.add_argument('--sha1')

    # check ###################################################################
    check_parser = sub_parser.add_parser('check')

    add_common_args(check_parser)

    check_parser.add_argument(
        '--required-sections',
        nargs='+',
    )

    # releases ################################################################
    releases_parser = sub_parser.add_parser('releases')

    add_common_args(releases_parser)

    releases_parser.add_argument(
        '--release-tag-pattern',
    )

    releases_parser.add_argument(
        '--as-ranges',
        action='store_true',
    )

    releases_parser.add_argument(
        '--include-unmerged',
        action='store_true',
    )

    # changelog ###############################################################
    changelog_parser = sub_parser.add_parser('changelog')

    add_common_args(changelog_parser)

    changelog_parser.add_argument(
        'ranges',
        nargs='*',
    )

    changelog_parser.add_argument(
        '--sections',
        nargs='+',
        default=['breaking-changes', 'changes', 'bug-fixes'],
    )

    # find ####################################################################
    find_parser = sub_parser.add_parser('find')

    add_common_args(find_parser)

    find_parser.add_argument('range')

    find_parser.add_argument(
        '--flags',
        nargs='+',
    )

    # parse args ##############################################################
    namespace = parser.parse_args(args=argv[1:])
    args = {}

    for key, value in vars(namespace).items():
        key = key.replace('_', '-')
        args[key] = value

    return args


def handle_commandline(argv, setup_logging=False):
    args = parse_command_line_args(argv=argv)
    exception = None

    # setup logging
    if setup_logging:
        simple_logging_setup.setup(
            preset='cli',
            level=args['log-level'],
            loggers=args['loggers'],
        )

    # read config
    config_root, config = get_config()

    # run command
    command = COMMANDS[args['command']]
    exception = None

    try:
        command(
            cli_args=args,
            config_root=config_root,
            config=config,
        )

    except Exception as e:
        exception = e

    # exit code / traceback
    if not exception:
        return 0

    if args['traceback']:
        raise exception

    else:
        print(exception)

    return 1
