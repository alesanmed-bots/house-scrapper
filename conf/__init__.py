# coding:utf-8
import toml
import os

config = None

def get_config():
    global config
    dirname = os.path.dirname(__file__)

    if not config:
        config = toml.load(os.path.join(dirname, 'vars.toml'))

        env = config['environment']

        config = config['environments'][env]
        config['environment'] = env

        config['ROOT_DIR'] = os.path.normpath(os.path.join(dirname, '..'))

    return config
