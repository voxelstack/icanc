import click
import os
import pyperclip
import subprocess
import tomllib

from .tools.preprocessor import preprocess

@click.command()
@click.argument("judge", type=str)
@click.argument("problem", type=str)
@click.option("--solution", "solution_src", default="solution")
@click.option("--open", "open_editor", is_flag=True)
@click.option("--copy", is_flag=True)
def submit(judge, problem, solution_src, open_editor, copy):
    with open(os.path.join(os.getcwd(), "iccrc.toml"), "rb") as f:
        cfg = tomllib.load(f)
    
    solution_dir = os.path.join(os.getcwd(), "problems", judge, problem)
    solution_path = os.path.join(solution_dir, "{}.c".format(solution_src))
    if not os.path.exists(solution_path):
        click.echo("Problem {}/{} does not exist.".format(judge, problem), err=True)
        exit(1)

    submission = preprocess(solution_path)

    submission_dir = os.path.join(os.getcwd(), "submissions", judge, problem)
    submission_path = os.path.join(submission_dir, "{}.c".format(solution_src))
    os.makedirs(submission_dir, exist_ok=True)

    with open(submission_path, "w") as f:
        f.write(submission)

    if open_editor:
        subprocess.run([cfg["editor"], submission_path])

    if copy:
        pyperclip.copy(submission)
