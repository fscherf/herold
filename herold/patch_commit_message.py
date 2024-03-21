from herold.meta_data import extract, generate, insert


def patch_commit_message(cli_args, config_root, config):

    # read commit message prepared by git
    commit_message_path = cli_args['commit-message-file']
    commit_message_lines = open(commit_message_path, 'r').read().splitlines()

    # add meta data block if needed
    meta_data = extract(commit_message_lines)

    if not meta_data:
        meta_data_lines = generate(
            config_root=config_root,
            config=config,
        )

        insert(
            commit_message_lines=commit_message_lines,
            meta_data_lines=meta_data_lines,
        )

    # write commit message
    with open(commit_message_path, 'w') as file_handle:
        file_handle.write('\n'.join(commit_message_lines))
