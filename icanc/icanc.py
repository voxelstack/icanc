import click

from .commands.create import create, scaffold
from .commands.init import init
from .commands.submit import submit
from .commands.test import test
from .commands.ci import ci

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
    icanc()

if __name__ == '__main__':
    main()
