import click
import os
import shutil
import subprocess
import tomllib

@click.group()
def create():
    pass

@create.command()
@click.argument("judge", type=str)
@click.argument("problem", type=str)
@click.option("--template", type=click.Path(exists=True))
@click.option("--solution", "solution_dst", default="solution")
@click.option("--open", "open_editor", is_flag=True)
def solution(**kwargs):
    create_solution(**kwargs)

def create_solution(judge, problem, template, solution_dst, open_editor):
    with open(os.path.join(os.getcwd(), "iccrc.toml"), "rb") as f:
        cfg = tomllib.load(f)
    
    dir = os.path.join(os.getcwd(), "problems", judge, problem)
    os.makedirs(dir, exist_ok=True)

    solution_path = os.path.join(dir, "{}.c".format(solution_dst))
    shutil.copy2(template, solution_path)
    
    click.echo("Created blank solution: ./problems/{}/{}/{}.c".format(judge, problem, solution_dst))

    if open_editor:
        subprocess.run([cfg["editor"], solution_path])

@create.command()
@click.argument("judge", type=str)
@click.argument("problem", type=str)
@click.option("--open", "open_editor", is_flag=True)
@click.option("--testcases", "testcases_dst", default="testcases")
def testcases(**kwargs):
    create_testcases(**kwargs)

def create_testcases(judge, problem, testcases_dst, open_editor):
    with open(os.path.join(os.getcwd(), "iccrc.toml"), "rb") as f:
        cfg = tomllib.load(f)
    
    dir = os.path.join(os.getcwd(), "problems", judge, problem)
    if not os.path.exists(dir):
        click.echo("Problem {}/{} does not exist.".format(judge, problem), err=True)
        exit(1)
    os.makedirs(dir, exist_ok=True)

    testcases_path = os.path.join(dir, "{}.toml".format(testcases_dst))
    
    with open(testcases_path, "w") as f:
        f.writelines([
            "# {}/{}\n\n".format(judge, problem),
            "[case1]\n",
            "in = \"\"\"\"\"\"\n",
            "out = \"\"\"\"\"\"\n"
        ])

    click.echo("Created blank testcases: ./problems/{}/{}/{}.toml".format(judge, problem, testcases_dst))

    if open_editor:
        subprocess.run([cfg["editor"], testcases_path])

@click.command()
@click.argument("judge", type=str)
@click.argument("problem", type=str)
@click.option("--template", type=click.Path(exists=True))
@click.option("--solution", "solution_dst", default="solution")
@click.option("--testcases", "testcases_dst", default="testcases")
@click.option("--open", "open_editor", is_flag=True)
def scaffold(judge, problem, template, solution_dst, testcases_dst, open_editor):
    click.echo("Scaffolding {}/{}\n".format(judge, problem))

    create_solution(judge, problem, template, solution_dst, open_editor)
    create_testcases(judge, problem, testcases_dst, False)
