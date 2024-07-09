import click
import os
from .submit import handle_submit
import time
from .tools.builder import build
from .tools.runner import run
from .tools.writer import present_cases
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

@click.command()
@click.argument("judge", type=str)
@click.argument("problem", type=str)
@click.option("--solution", "solution_src", default="solution")
@click.option("--testcases", "testcases_src", multiple=True)
@click.option("--watch", is_flag=True)
def test(**kwargs):
    handle_test(**kwargs)

def handle_test(judge, problem, solution_src, testcases_src, watch):
    solution_dir = os.path.join(os.getcwd(), "problems", judge, problem)
    solution_path = os.path.join(solution_dir, f"{solution_src}.c")
    submission_dir = os.path.join(os.getcwd(), "submissions", judge, problem)
    submission_path = os.path.join(submission_dir, "{}.c".format(solution_src))
    
    include_dir = os.path.join(os.getcwd(), "include")
    binary_dir = os.path.join(os.getcwd(), "binaries", judge, problem)
    binary_path = os.path.join(binary_dir, solution_src)
    os.makedirs(binary_dir, exist_ok=True)

    testcases_dir = os.path.join(os.getcwd(), "problems", judge, problem) 

    # click.clear() leaves uncleared lines if files change too fast.
    def clear():
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def test():
        clear()
        if watch:
            click.secho(" WATCH ", bg="cyan", fg="white", nl=False)
        else:
            click.secho(" RUN ", bg="cyan", fg="white", nl=False)
        click.echo(f" ./problems/{judge}/{problem}/", nl=False)
        click.secho(f"{solution_src}.c", bold=True)

        # TODO Only rebuild the list of testcases when a file is created or deleted.
        testcases = []
        if testcases_src:
            testcases.extend([f"{t}.toml" for t in testcases_src])
        else:
            files = os.listdir(testcases_dir)
            testcases.extend([f for f in files if f.endswith(".toml")])

        for testcase in testcases:
            click.echo(f"\n< ./problems/{judge}/{problem}/{testcase}")

            handle_submit(judge, problem, f"{solution_src}.c", False, False)
            
            result = build(solution_path, submission_path, binary_path)
            if result != 0:
                return

            testcase_path = os.path.join(testcases_dir, testcase)
            runs = run(binary_path, testcase_path)
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
