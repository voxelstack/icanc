import os
from .exception import NotFoundException
from importlib.resources import files
from .rc import preload_rc

cwd = os.getcwd()
dirs = [
    "include",
    "problems",
    "templates",
    "submissions",
    "binaries",
]
paths = [os.path.join(cwd, dir) for dir in dirs]
icc_dirs = dict(zip(dirs, paths))

def ensure_paths():
    for dir in paths:
        os.makedirs(dir, exist_ok=True)

def icanc_path(dir, *argv):
    path = icc_dirs.get(dir)
    
    for arg in argv:
        path = os.path.join(path, arg)

    return path

def data_path(path):
    return files("icanc.data").joinpath(path)

def ensure_cwd():
    if not os.path.exists(os.path.join(cwd, "icancrc.toml")):
        raise NotFoundException("config", "icancrc.toml", "Are you running from the project root?")
    
    preload_rc()
