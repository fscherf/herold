import yaml

from herold.utils.templating import render_template


def generate(config_root, config, template_name='meta-data.yml'):
    text = render_template(
        config_root=config_root,
        config=config,
        template_name=template_name,
    )

    return text.strip().splitlines()


def extract(commit_message_lines, root='meta'):
    start_marker = f'{root}:'
    start_index = None
    stop_index = len(commit_message_lines)

    # find start index
    for index, line in enumerate(commit_message_lines):
        if line.strip().startswith(start_marker):
            start_index = index

            break

    # nothing found
    if start_index is None:
        return

    # find stop index
    for index, line in enumerate(commit_message_lines[start_index+1:]):
        if not line:
            continue

        if line[0] not in (' ', '\t'):
            stop_index = start_index + index + 1

            break

    # parse yaml
    yaml_text = '\n'.join(commit_message_lines[start_index:stop_index])

    try:
        return yaml.safe_load(yaml_text)[root]

    except yaml.YAMLError:
        return


def insert(commit_message_lines, meta_data_lines=None):
    if not meta_data_lines:
        meta_data_lines = generate()

    # find start index
    start_index = 0

    for index, line in enumerate(commit_message_lines):
        line = line.strip()

        if line.startswith('Signed-off-by:') or line.startswith('#'):
            start_index = index

            break

    # concat preexisting commit message and meta data block
    lines = [
        *commit_message_lines[0:start_index],
        *meta_data_lines,
        '',
        *commit_message_lines[start_index:],
    ]

    # update commit_message_line
    commit_message_lines.clear()
    commit_message_lines.extend(lines)

    return commit_message_lines
