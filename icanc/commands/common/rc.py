import os
import tomllib

config = dict(
    author = None,
    email = None,
    repository = None,
    editor = "code.cmd",
    compiler = "gcc",
    udebug = None
)

def preload_rc():
    global config

    with open(os.path.join(os.getcwd(), "icancrc.toml"), "rb") as f:
        config_file = tomllib.load(f)
        config.update(**config_file)
