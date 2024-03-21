import os

from jinja2 import Template


def render_template(config_root, config, template_name, template_context=None):
    template_path = os.path.join(config_root, template_name)
    template_text = open(template_path, 'r').read()

    template = Template(template_text)

    return template.render(**{
        'config_root': config_root,
        'config': config,
        **(template_context or {}),
    })
