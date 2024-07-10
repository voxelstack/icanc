import click

def present_cases(cases):
    if len(cases) == 0:
        click.secho(" NO TESTS ", bg="yellow", fg="black")
        return -1
    
    fails = []
    for case in cases:
        name = case["name"]
        error = case["error"]

        if error == None:
            click.secho("  ✓ ", fg="green", nl=False)
            click.secho(name, bold=True)
            continue

        if error == "invalid_case":
            click.secho("  ⚠ ", fg="red", nl=False)
            click.secho(name, bold=True, nl=False)
            click.echo(" (invalid testcase)")
        elif error == "runtime":
            click.secho("  ⚠ ", fg="red", nl=False)
            click.secho(name, bold=True, nl=False)
            click.echo(" (runtime error)")
        elif error == "presentation":
            click.secho("  × ", fg="yellow", nl=False)
            click.secho(name, bold=True)
        elif error == "wrong_answer":
            click.secho("  × ", fg="red", nl=False)
            click.secho(name, bold=True)
        
        fails.append(case)
    
    if len(fails) == 0:
        click.secho(" PASS ", bg="green", fg="black")
    else:
        click.secho(" FAIL ", bg="red", fg="black")
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

def present_ci_cases(cases):
    if len(cases) == 0:
        click.echo("      NO TESTS")
        return -1
    
    fails = []
    for case in cases:
        name = case["name"]
        error = case["error"]

        if error == None:
            click.echo(f"      ✓ {name}")
            continue

        if error == "invalid_case":
            click.echo(f"      ⚠ {name} (invalid testcase)")
        elif error == "runtime":
            click.secho(f"      ⚠ {name} (runtime error)")
        elif error == "presentation":
            click.secho(f"      × {name}")
        elif error == "wrong_answer":
            click.secho(f"      × {name}")
        
        fails.append(case)
