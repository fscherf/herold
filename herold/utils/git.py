from herold.utils._subprocess import run


def get_commit_message(commit_hash, format="%B", cwd=None):
    return run(
        command=f'git show -s {commit_hash} --format="{format}"',
        cwd=cwd,
    )[1]


def get_commit_hashes(range_as_string, format='%h', cwd=None):
    return run(
        command=f'git log {range_as_string} --format={format}',
        cwd=cwd,
    )[1]


def get_tags(merged=False, cwd=None):
    command = ['git', 'tag', '--sort=taggerdate']

    if merged:
        command.append('--merged')

    return run(command=command, cwd=cwd)[1]


def get_tag_date(tag_name, cwd=None):
    exit_code, lines = run(
        command=f'git log -1 {tag_name} --format=%as',
        cwd=cwd,
    )

    if exit_code > 0 or len(lines) < 1:
        return ''

    return lines[0]


def get_top_level(cwd=None):
    exit_code, lines = run(
        command='git rev-parse --show-toplevel',
        cwd=cwd,
    )

    if exit_code > 0 or len(lines) < 1:
        return ''

    return lines[0]
