import click

from commands.create import create, scaffold
from commands.init import init
from commands.submit import submit

@click.group()
def icc():
    pass

icc.add_command(init)
icc.add_command(create)
icc.add_command(scaffold)
icc.add_command(submit)

if __name__ == '__main__':
    icc()
