import click
import os
import shutil
import subprocess
from .common.exception import FoundException, InvalidCommandException, NotFoundException
from .common.paths import ensure_cwd, ensure_paths, icanc_path
from .common.rc import config
from .tools.udebug import fetch_testcases

@click.group()
def create():
    """Create solutions or testcases."""
    pass

@create.command()
@click.argument("judge", type=str)
@click.argument("problem", type=str)
@click.option("-t", "--template", type=str, default="main")
@click.option("-s", "--solution", "solution_dst", default="solution", help="Name for the solution file.")
@click.option("-e", "--edit", "open_editor", is_flag=True, help="Open solution file on text editor.")
def solution(**kwargs):
    create_solution(**kwargs)

def create_solution(judge, problem, template, solution_dst, open_editor):
    ensure_cwd()
    ensure_paths()

    template_filename = f"{template}.c"
    template_path = icanc_path("templates", template_filename)
    if not os.path.exists(template_path):
        raise NotFoundException("template", f"./templates/{template_filename}")
    
    dir = icanc_path("problems", judge, problem)
    os.makedirs(dir, exist_ok=True)

    solution_filename = f"{solution_dst}.c"
    solution_path_rel = f"./problems/{judge}/{problem}/{solution_filename}"
    solution_path = icanc_path("problems", judge, problem, solution_filename)
    if os.path.exists(solution_path):
        raise FoundException("solution", solution_path_rel, "To create multiple solutions set the solution name with the --solution option.")
    shutil.copy2(template_path, solution_path)
    
    click.echo(f"Created blank solution: {solution_path_rel}")

    if open_editor:
        subprocess.run([config["editor"], solution_path])

@create.command()
@click.argument("judge", type=str)
@click.argument("problem", type=str)
@click.option("-t", "--testcases", "testcases_dst", default="testcases", help="Name for the testcases file.")
@click.option("-e", "--edit", "open_editor", is_flag=True, help="Open testcases file on text editor.")
@click.option("-u", "--udebug", "udebug", is_flag=True, help="Download testcases from udebug.")
def testcases(**kwargs):
    create_testcases(**kwargs)

def create_testcases(judge, problem, testcases_dst, open_editor, udebug):
    if (not udebug and testcases_dst == "udebug"):
        raise InvalidCommandException("udebug.toml is reserved for udebug testcases", "Change the value of --testcases to something else.")
    
    testcases_set = click.get_current_context().get_parameter_source("testcases_dst") != click.core.ParameterSource.DEFAULT
    if (udebug and testcases_set and testcases_dst != "udebug"):
        raise InvalidCommandException("udebug testcases must be called udebug.toml", "You can leave --testcases unset when creating udebug testcases.")

    ensure_cwd()
    ensure_paths()
    
    dir = icanc_path("problems", judge, problem)
    if not os.path.exists(dir):
        raise NotFoundException("problem", f"{judge}/{problem}")

    if udebug:
        testcases_path = create_udebug_testcases(judge, problem)
    else:
        testcases_path = create_blank_testcases(judge, problem, testcases_dst)

    if open_editor:
        subprocess.run([config["editor"], testcases_path])

def create_blank_testcases(judge, problem, testcases_dst):
    testcases_filename = f"{testcases_dst}.toml"
    testcases_path_rel = f"./problems/{judge}/{problem}/{testcases_filename}"
    testcases_path = icanc_path("problems", judge, problem, testcases_filename)
    if os.path.exists(testcases_path):
        raise FoundException("testcases", testcases_path_rel, "To create multiple testcases set the solution name with the --testcases option.")

    with open(testcases_path, "w", encoding="utf-8") as f:
        f.writelines([
            "# {}/{}\n\n".format(judge, problem),
            "[case1]\n",
            "in = \"\"\"\"\"\"\n",
            "out = \"\"\"\"\"\"\n"
        ])

    click.echo(f"Created blank testcases: {testcases_path_rel}")

    return testcases_path

def create_udebug_testcases(judge, problem):
    testcases_filename = f"udebug.toml"
    testcases_path_rel = f"./problems/{judge}/{problem}/{testcases_filename}"
    testcases_path = icanc_path("problems", judge, problem, testcases_filename)

    with open(testcases_path, "w") as f:
        header = f"# {judge}/{problem}\n# udebug.com\n\n"
        testcases = fetch_testcases(judge, problem)
        f.write(header + testcases)

    click.echo(f"Downloaded udebug testcases: {testcases_path_rel}")
    click.echo(f"\nRemember to vote on useful inputs!")
    click.echo(f"https://www.udebug.com/?search_string={problem}&search_category=0")

    return testcases_path

@click.command()
@click.argument("judge", type=str)
@click.argument("problem", type=str)
@click.option("-t", "--template", type=str, default="main")
@click.option("--solution", "solution_dst", default="solution", help="Name for the solution file.")
@click.option("--testcases", "testcases_dst", default="testcases", help="Name for the testcases file.")
@click.option("-e", "--edit", "open_editor", is_flag=True, help="Open solution file on text editor.")
def scaffold(judge, problem, template, solution_dst, testcases_dst, open_editor):
    """Create a solution and testcase files."""
    
    click.echo("Scaffolding {}/{}\n.".format(judge, problem))
    create_solution(judge, problem, template, solution_dst, open_editor)
    create_testcases(judge, problem, testcases_dst, False, False)
