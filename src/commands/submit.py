import click
import os
import pyperclip
import subprocess
import tomllib

from .tools.preprocessor import preprocess

@click.command()
@click.argument("judge", type=str)
@click.argument("problem", type=str)
@click.option("--solution", "solution_src", default="solution", help="Which solution file to submit.")
@click.option("--open", "open_editor", is_flag=True, help="Open submission file on text editor.")
@click.option("--copy", is_flag=True, help="Copy submission to clipboard.")
def submit(**kwargs):
    """Bundle solution into a single source file for submission."""

    handle_submit(**kwargs)

def handle_submit(judge, problem, solution_src, open_editor, copy):
    with open(os.path.join(os.getcwd(), "iccrc.toml"), "rb") as f:
        cfg = tomllib.load(f)
    
    solution_dir = os.path.join(os.getcwd(), "problems", judge, problem)
    solution_path = os.path.join(solution_dir, f"{solution_src}.c")
    if not os.path.exists(solution_path):
        click.echo("Problem {}/{} does not exist.".format(judge, problem), err=True)
        exit(1)

    submission = preprocess(solution_path)

    submission_dir = os.path.join(os.getcwd(), "submissions", judge, problem)
    submission_path = os.path.join(submission_dir, f"{solution_src}.c")
    os.makedirs(submission_dir, exist_ok=True)

    with open(submission_path, "w") as f:
        f.write(submission)

    if open_editor:
        subprocess.run([cfg["editor"], submission_path])

    if copy:
        pyperclip.copy(submission)
