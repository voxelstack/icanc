import os
import tomllib

config = dict(
    editor = "code.cmd",
    compiler = "gcc",
)

def preload_rc():
    global config

    with open(os.path.join(os.getcwd(), "icancrc.toml"), "rb") as f:
        config_file = tomllib.load(f)
        config = config | config_file
