import click
import os
from pathlib import Path
from .submit import handle_submit
import sys
from .tools.builder import build
from .common.paths import ensure_cwd, ensure_paths, icanc_path
from .tools.runner import run
from .tools.writer import present_ci_cases

@click.command()
@click.option("-j", "--judge", type=str, help="Only test one judge.")
def ci(**kwargs):
    """Test everything with machine friendly output and exit codes."""
    handle_ci(**kwargs)

def handle_ci(judge):
    ensure_cwd()
    ensure_paths()

    problems_dir = icanc_path("problems")

    judges = []
    if judge:
        judges.append(judge)
    else:
        judges = os.listdir(problems_dir)
    
    failed = 0
    for judge in judges:
        failed_judge = 0
        judge_dir = icanc_path("problems", judge)
        problems = os.listdir(judge_dir)
        
        for problem in problems:
            failed_problem = 0
            problem_dir = icanc_path("problems", judge, problem)
            solutions = [s for s in os.listdir(problem_dir) if s.endswith(".c")]

            click.echo(f"{judge}/{problem}")
            
            for solution in solutions:
                failed_solution = 0
                click.secho(f"  ./problems/{judge}/{problem}/{solution}")
                testcases = [s for s in os.listdir(problem_dir) if s.endswith(".toml")]

                solution_path = icanc_path("problems", judge, problem, solution)
                submission_path = icanc_path("submissions", judge, problem, solution)
                binary_dir = icanc_path("binaries", judge, problem)
                binary_path = icanc_path("binaries", judge, Path(solution).stem)
                os.makedirs(binary_dir, exist_ok=True)

                handle_submit(judge, problem, Path(solution).stem, False, False)
                result = build(solution_path, submission_path, binary_path)
                if result != 0:
                    return -1

                for testcase in testcases:
                    click.echo(f"    < ./problems/{judge}/{problem}/{testcase}")
                    
                    testcase_path = icanc_path("problems", judge, problem, testcase)
                    runs = run(binary_path, testcase_path)
                    failed_solution += sum(1 if r["error"] is not None else 0 for r in runs)
                    present_ci_cases(runs)
                failed_problem += failed_solution
            failed_judge += failed_problem
        failed += failed_judge
    
    if failed == 0:
        click.echo("PASS")
    sys.exit(failed)
