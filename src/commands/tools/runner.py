import tomllib
import click
import difflib
import os
import subprocess

def run(binary, testcases):
    with open(testcases, "rb") as f:
        cases = tomllib.load(f).items()
        fails = []

        if len(cases) == 0:
            click.secho(" NO TESTS ", bg="yellow", fg="black")
            return -1


        for name, case in cases:
            if "in" not in case or "out" not in case:
                click.secho("⚠ ", fg="red", nl=False)
                click.secho(name, bold=True, nl=False)
                click.echo(" (invalid testcase)")
                fails.append({
                    "name": name,
                    "error": "invalid_case",
                })
                continue

            result = subprocess.run(
                binary,
                input=case.get("in"),
                capture_output=True,
                text=True,
                env=dict(os.environ, LIBC_FATAL_STDERR_="1")
            )

            if result.returncode != 0:
                click.secho("⚠ ", fg="red", nl=False)
                click.secho(name, bold=True, nl=False)
                click.echo(" (runtime error)")

                fails.append({
                    "name": name,
                    "error": "runtime",
                    "stderr": result.stderr,
                })
                continue

            actual = result.stdout
            expected = case.get("out")
            if expected == actual:
                click.secho("✓ ", fg="green", nl=False)
                click.secho(name, bold=True)
            else:
                

                diff = difflib.unified_diff(expected.splitlines(), actual.splitlines(), fromfile="expected", tofile="received", lineterm="")
                line = next(diff, None)
                if line is None:
                    click.secho("× ", fg="yellow", nl=False)
                    fails.append({
                        "name": name,
                        "error": "presentation",
                    })
                else:
                    click.secho("× ", fg="red", nl=False)
                    fail_diff = [line]
                    for l in diff:
                        fail_diff.append(l)

                    fails.append({
                        "name": name,
                        "error": "wrong_answer",
                        "diff": fail_diff
                    })
                click.secho(name, bold=True)

        if len(fails) == 0:
            click.secho("\n PASS ", bg="green", fg="black")
            return 0
        
        click.secho("\n FAIL ", bg="red", fg="black")
        for fail in fails:
            name = fail["name"]
            error = fail["error"]

            click.echo()
            if error == "presentation":
                click.secho("● ", fg="yellow", nl=False)
                click.secho(f"{name}: presentation error")
            elif error == "wrong_answer":
                diff = fail["diff"]

                click.secho("● ", fg="red", nl=False)
                click.secho(f"{name}: wrong answer")
                for line in diff:
                    color = "red" if line.startswith("-") else "green" if line.startswith("+") else None
                    click.secho(f"{line}", fg=color)
            elif error == "runtime":
                stderr = fail["stderr"]

                click.secho("● ", fg="red", nl=False)
                click.secho(f"{name}: runtime error")
                click.echo(stderr)
            elif error == "invalid_case":
                click.secho(f"{name}: invalid test case", fg="red")
        
        
        return len(fails)
