import os
from jinja_macro_tags import configure_environment


def autoload_macros(environment, macros_folder):
    env = environment
    configure_environment(env, with_jinja_tags=False, with_html_tags=True)
    env.macros.register_directory(macros_folder)