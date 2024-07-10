import click
import os
import pyperclip
import subprocess
import tomllib
from .common.exception import NotFoundException
from .common.paths import ensure_cwd, ensure_paths, icanc_path
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
    ensure_cwd()
    ensure_paths()
    
    with open(os.path.join(os.getcwd(), "icancrc.toml"), "rb") as f:
        cfg = tomllib.load(f)
    
    solution_filename = f"{solution_src}.c"
    solution_path_rel = f"./{judge}/{problem}/{solution_filename}"
    solution_path = icanc_path("problems", judge, problem, solution_filename)
    if not os.path.exists(solution_path):
        raise NotFoundException("solution", solution_path_rel)
    submission = preprocess(solution_path)

    submission_dir = icanc_path("submissions", judge, problem)
    submission_path = icanc_path("submissions", judge, problem, solution_filename)
    os.makedirs(submission_dir, exist_ok=True)

    with open(submission_path, "w") as f:
        f.write(submission)

    if open_editor:
        subprocess.run([cfg["editor"], submission_path])

    if copy:
        pyperclip.copy(submission)
