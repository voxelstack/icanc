import click
import os
import shutil
import subprocess

@click.command()
@click.option("--name", prompt=True, default="leet")
def init(name):
    """Initialize an empty icanc project."""

    dir = os.path.join(os.getcwd(), name)
    if os.path.exists(dir):
        click.echo("Directory ./{} already exists.".format(name), err=True)
        exit(1)
    os.makedirs(dir)

    res_dir = os.path.join(os.path.dirname(__file__), "..", "data")

    os.makedirs(os.path.join(dir, "problems"))
    shutil.copy2(os.path.join(res_dir, "icancrc.toml"), dir)
    shutil.copy2(os.path.join(res_dir, "LICENSE"), dir)
    shutil.copytree(os.path.join(res_dir, "include"), os.path.join(dir, "include"))
    shutil.copytree(os.path.join(res_dir, "templates"), os.path.join(dir, "templates"))
    with open(os.path.join(res_dir, "README.md"), "r") as src:
        readme = src.read().format(name=name)
        with open(os.path.join(dir, "README.md"), "w") as dst:
            dst.write(readme)
    
    click.echo("\nInitialized icanc project at ./{}".format(name))
    click.echo("Get started with cd ./{} && icanc --help".format(name))

def read_git_config(config):
    res = subprocess.run(["git", "config", config], stdout=subprocess.PIPE)
    if res.returncode == 0:
        return res.stdout.rstrip().decode()
    return ""
