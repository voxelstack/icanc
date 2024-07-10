import click
import sys

from .commands.create import create, scaffold
from .commands.init import init
from .commands.submit import submit
from .commands.test import test
from .commands.ci import ci
from .commands.common.exception import IcancException

@click.group()
def icanc():
    pass

icanc.add_command(init)
icanc.add_command(create)
icanc.add_command(scaffold)
icanc.add_command(submit)
icanc.add_command(test)
icanc.add_command(ci)

def main():
    try:
        icanc()
        sys.exit(0)
    except IcancException as e:
        click.secho(f"Error: {e.error}: {e.message}", err=True)
        if e.hint:
            click.secho(e.hint)
        sys.exit(-1)


if __name__ == '__main__':
    main()
