import click
import os
from .submit import handle_submit
from .tools.builder import build
from .tools.runner import run

@click.command()
@click.argument("judge", type=str)
@click.argument("problem", type=str)
@click.option("--solution", "solution_src", default="solution")
@click.option("--testcases", "testcases_src", default="testcases")
@click.option("--watch", is_flag=True)
def test(**kwargs):
    handle_test(**kwargs)

def handle_test(judge, problem, solution_src, testcases_src, watch):
    click.clear()

    handle_submit(judge, problem, solution_src, False, False)
    solution_path = os.path.join(os.getcwd(), "problems", judge, problem, f"{solution_src}.c")
    submission_dir = os.path.join(os.getcwd(), "submissions", judge, problem)
    submission_path = os.path.join(submission_dir, "{}.c".format(solution_src))
    
    binary_dir = os.path.join(os.getcwd(), "binaries", judge, problem)
    os.makedirs(binary_dir, exist_ok=True)
    
    binary_path = os.path.join(binary_dir, solution_src)
    result = build(solution_path, submission_path, binary_path)
    if result != 0:
        return

    testcases_dir = os.path.join(os.getcwd(), "problems", judge, problem)
    testcases_path = os.path.join(testcases_dir, "{}.toml".format(testcases_src))

    click.secho(" RUN ", bg="cyan", fg="white", nl=False)
    click.echo(f" ./problems/{judge}/{problem}/", nl=False)
    click.secho(f"{solution_src}.c", bold=True, nl=False)
    click.echo(f" < ./problems/{judge}/{problem}/{testcases_src}.toml\n")

    run(binary_path, testcases_path)
