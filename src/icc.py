import click

from commands.create import create, scaffold
from commands.init import init

@click.group()
def icc():
    pass

icc.add_command(init)
icc.add_command(create)
icc.add_command(scaffold)

if __name__ == '__main__':
    icc()
