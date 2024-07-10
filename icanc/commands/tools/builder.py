import click
import os
import subprocess
from ..common.rc import config

def build(src_path, submission_path, bin_path):
    result = subprocess.run(
        [
            config["compiler"],
            submission_path,
            "-o", bin_path,
            "-I", os.path.join(os.getcwd(), "include")
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        click.secho(" Build failed ", bg="red", fg="black", err=True)
        # The compiler errors will point to the submission.
        # Print the actual source so you can navigate to it.
        click.echo(src_path)
        click.echo()
        click.echo(result.stderr, err=True)
    
    return result.returncode
