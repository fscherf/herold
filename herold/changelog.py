import logging

from herold.utils.git import get_commit_hashes, get_commit_message
from herold.utils.templating import render_template
from herold.meta_data import extract

logger = logging.getLogger('herold.changelog')


def _get_commit_hashes_for_range(range_as_string):
    commit_hashes = []

    for line in get_commit_hashes(range_as_string, format='%h,%H')[::-1]:
        short_hash, long_hash = line.split(',')

        commit_hashes.append(
            (short_hash, long_hash),
        )

    return commit_hashes


def _get_commit_hash_index(commit_hashes, commit_hash):
    for index, (short_hash, long_hash) in enumerate(commit_hashes):
        if commit_hash == short_hash or commit_hash == long_hash:
            return index

    return -1


def _extract_changelog_entries_from_range(range_as_string, sections):
    # extract meta data blocks from range
    logger.debug('extracting changelog from range %s', range_as_string)

    commit_hashes = _get_commit_hashes_for_range(range_as_string)
    meta_data = []

    for short_hash, long_hash in commit_hashes:
        commit_message_lines = get_commit_message(short_hash)
        _meta_data = extract(commit_message_lines)

        if not _meta_data or 'changelog' not in _meta_data:
            meta_data.append(None)

            continue

        meta_data.append(_meta_data)

    # removing revoked meta data blocks
    for meta_data_index, _meta_data in enumerate(meta_data):
        if (not _meta_data or
                'revokes' not in _meta_data['changelog'] or
                not _meta_data['changelog']['revokes']):

            continue

        for revoked_commit_hash in _meta_data['changelog']['revokes']:
            commit_hash_index = _get_commit_hash_index(
                commit_hashes=commit_hashes,
                commit_hash=revoked_commit_hash,
            )

            if commit_hash_index == -1:
                logger.warning(
                    '%s: revoked hash "%s" is not in range "%s"',
                    commit_hashes[meta_data_index][0],
                    revoked_commit_hash,
                    range_as_string,
                )

            meta_data[commit_hash_index] = None

    # extract entries form meta data blocks
    entries = {
        key: [] for key in sections
    }

    for index, _meta_data in enumerate(meta_data):
        if not _meta_data:
            continue

        for section in sections:
            if section not in _meta_data['changelog']:
                continue

            lines = _meta_data['changelog'][section]

            for line in lines:
                line.strip()

                if not line:
                    continue

                entries[section].append(
                    (line, commit_hashes[index][0]),
                )

    # remove empty entries
    for key, value in entries.copy().items():
        entries[key] = [i for i in value if i]

        if not entries[key]:
            entries.pop(key)

    return entries


# cli entry point
def changelog(cli_args, config_root, config):
    ranges_as_strings = cli_args['ranges'] or []
    sections = cli_args['sections']

    # split ranges and range names
    for index, range_as_string in enumerate(ranges_as_strings.copy()):
        if ':' in range_as_string:
            ranges_as_strings[index] = tuple(range_as_string.split(':', 1))

        else:
            ranges_as_strings[index] = (
                range_as_string, range_as_string,
            )

    # collect changelog data
    changelog = {
        'sections': [
            (name, config['changelog']['sections'].get(name, name))
            for name in sections
        ],
        'ranges': [],
    }

    for range_name, range_as_string in ranges_as_strings:
        changelog['ranges'].append({
            'range_as_string': range_as_string,
            'name': range_name,
            'entries': _extract_changelog_entries_from_range(
                range_as_string=range_as_string,
                sections=sections,
            ),
        })

    # render template
    logger.debug('rendering changelog')

    changelog_text = render_template(
        config_root=config_root,
        config=config,
        template_name='changelog',
        template_context={
            'changelog': changelog,
        },
    )

    logger.debug('writing changelog to stdout')

    print(changelog_text)
