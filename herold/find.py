from herold.utils.git import get_commit_hashes, get_commit_message
from herold.meta_data import extract


def find(cli_args, config_root, config):
    range_as_string = cli_args['range']
    flags = set(cli_args['flags'] or [])

    if not flags:
        raise RuntimeError('no flags specified')

    for commit_hash in get_commit_hashes(range_as_string)[::-1]:
        commit_message_lines = get_commit_message(commit_hash)
        meta_data = extract(commit_message_lines)

        if 'flags' not in meta_data:
            continue

        if len(set(meta_data['flags']) & flags) < 1:
            continue

        print(get_commit_message(commit_hash, format='%h %s')[0])
