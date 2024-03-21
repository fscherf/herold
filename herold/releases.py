import re

from herold.utils.git import get_tags, get_commit_hashes


def get_release_tags(pattern, merged=False, cwd=None):
    regex = re.compile(pattern)
    release_tags = []

    for tag in get_tags(merged=merged, cwd=cwd):
        if not regex.match(tag):
            continue

        release_tags.append(tag)

    return release_tags


# cli entry point
def releases(cli_args, config_root, config):
    release_tag_pattern = (
        cli_args['release-tag-pattern'] or
        config['releases']['release-tag-pattern']
    )

    release_tags = get_release_tags(
        pattern=release_tag_pattern,
        merged=not cli_args['include-unmerged'],
    )

    # print plain list
    if not cli_args['as-ranges']:
        for release_tag in release_tags[::-1]:
            print(release_tag)

        return 0

    # print ranges
    ranges_as_strings = []

    for index in range(len(release_tags) - 1):
        ranges_as_strings.append(
            f'{release_tags[index+1]}:{release_tags[index]}..{release_tags[index+1]}',  # NOQA
        )

    # check for unreleased changes
    if release_tags:
        range_as_string = f'{release_tags[-1]}..HEAD'

        if get_commit_hashes(range_as_string):
            ranges_as_strings.append(
                f'Unreleased:{range_as_string}',
            )

    # write to stdout
    for range_as_string in ranges_as_strings[::-1]:
        print(range_as_string)

    return 0
