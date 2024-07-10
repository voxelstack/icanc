import click
import os
import shutil
import subprocess
from .common.exception import FoundException
from .common.paths import data_path

@click.command()
@click.option("--name", prompt=True, default="leet")
@click.option("--git", prompt="Initialize git repository", default=True, )
def init(**kwargs):
    """Initialize an icanc project."""
    handle_init(**kwargs)

def handle_init(name, git):
    dir = os.path.join(os.getcwd(), name)
    if os.path.exists(dir):
        raise FoundException("project", f"./{name}/")
    os.makedirs(dir)

    shutil.copy2(data_path("icancrc.toml"), dir)
    shutil.copy2(data_path("LICENSE"), dir)
    shutil.copytree(data_path("include"), os.path.join(dir, "include"))
    shutil.copytree(data_path("templates"), os.path.join(dir, "templates"))
    shutil.copytree(data_path("problems"), os.path.join(dir, "problems"))
    with open(data_path("README.md"), "r") as src:
        readme = src.read().format(name=name)
        with open(os.path.join(dir, "README.md"), "w") as dst:
            dst.write(readme)
    
    if git:
        shutil.copy2(data_path(".gitignore"), dir)
        subprocess.run(["git", "init", dir])
    
    click.secho("\n DONE ", bg="green", nl=False);
    click.secho(f" Your project was created at {name}/", fg="green")
    click.secho("Get started with",  nl=False)
    click.secho(f" cd {name} && icanc --help", bold=True)

def read_git_config(config):
    res = subprocess.run(["git", "config", config], stdout=subprocess.PIPE)
    if res.returncode == 0:
        return res.stdout.rstrip().decode()
    return ""
