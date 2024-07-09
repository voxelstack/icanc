import click
import os
import subprocess

def build(source, submission, binary):
    result = subprocess.run(
        [
            "gcc",
            submission,
            "-o", binary,
            "-I", os.path.join(os.getcwd(), "include")
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        click.secho(" Build failed ", bg="red", fg="black", err=True)
        # The compiler errors will point to the submission.
        # Print the actual source so you can navigate to it.
        click.echo(source)
        click.echo()
        click.echo(result.stderr, err=True)
    
    return result.returncode
