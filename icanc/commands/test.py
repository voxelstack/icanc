import click
import os
from .submit import handle_submit
import time
from .tools.builder import build
from .common.paths import ensure_cwd, ensure_paths, icanc_path
from .common.exception import NotFoundException
from .tools.runner import run
from .tools.writer import present_cases
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

@click.command()
@click.argument("judge", type=str)
@click.argument("problem", type=str)
@click.option("-s", "--solution", "solution_src", default="solution", help="Which solution to test.")
@click.option("-t", "--testcases", "testcases_src", multiple=True, help="Which testcases to test against.")
@click.option("-w", "--watch", is_flag=True, help="Rerun on changes to the problem or include directories.")
def test(**kwargs):
    """Test a solution against given testcases."""
    handle_test(**kwargs)

def handle_test(judge, problem, solution_src, testcases_src, watch):
    ensure_cwd()
    ensure_paths()
    
    solution_dir = icanc_path("problems", judge, problem)
    solution_filename = f"{solution_src}.c"
    solution_path = icanc_path("problems", judge, problem, solution_filename)
    submission_path = icanc_path("submissions", judge, problem, solution_filename)
    include_dir = icanc_path("include")
    binary_dir = icanc_path("binaries", judge, problem)
    binary_path = icanc_path("binaries", judge, problem, solution_src)
    testcases_dir = icanc_path("problems", judge, problem)
    os.makedirs(binary_dir, exist_ok=True)

    if not os.path.exists(solution_path):
        raise NotFoundException("solution", f"./problems/{judge}/{problem}/{solution_filename}")

    def clear():
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def test():
        # TODO Only rebuild the list of testcases when a file is created or deleted.
        testcases = []
        testcase_files = []
        if testcases_src:
            testcase_files.extend([f"{t}.toml" for t in testcases_src])
        else:
            files = os.listdir(testcases_dir)
            testcase_files.extend([f for f in files if f.endswith(".toml")])

        for testcase in testcase_files:
            path = icanc_path("problems", judge, problem, testcase)
            if not os.path.exists(path):
                raise NotFoundException("testcases", f"./problems/{judge}/{problem}/{testcase}")
            testcases.append({
                "name": testcase,
                "path": path
            })

        clear()
        if watch:
            click.secho(" WATCH ", bg="cyan", fg="white", nl=False)
        else:
            click.secho(" RUN ", bg="cyan", fg="white", nl=False)
        click.echo(f" ./problems/{judge}/{problem}/", nl=False)
        click.secho(solution_filename, bold=True)

        for testcase in testcases:
            click.echo(f"\n< ./problems/{judge}/{problem}/{testcase['name']}")

            handle_submit(judge, problem, solution_src, False, False)
            
            result = build(solution_path, submission_path, binary_path)
            if result != 0:
                return

            runs = run(binary_path, testcase["path"])
            present_cases(runs)

        if watch:
            click.echo("\nWatching for changes. ^C to stop.")

    class FileWatcher(FileSystemEventHandler):
        def __init__(self):
            FileSystemEventHandler.__init__(self)

        def on_modified(self, event):
            clear()
            test()

    if watch:
        watcher = FileWatcher()
        observer = Observer()
        observer.schedule(watcher, path=solution_dir, recursive=True)
        observer.schedule(watcher, path=include_dir, recursive=True)
        observer.start()

        try:
            test()
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
    else:
        test()
