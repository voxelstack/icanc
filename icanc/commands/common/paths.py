import os

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

for dir in paths:
    os.makedirs(dir, exist_ok=True)

def icanc_path(dir, *argv):
    path = icc_dirs.get(dir)
    
    for arg in argv:
        path = os.path.join(path, arg)

    return path
