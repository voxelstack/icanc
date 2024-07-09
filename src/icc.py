import click

from commands.create import create, scaffold
from commands.init import init
from commands.submit import submit
from commands.test import test

@click.group()
def icc():
    pass

icc.add_command(init)
icc.add_command(create)
icc.add_command(scaffold)
icc.add_command(submit)
icc.add_command(test)

if __name__ == '__main__':
    icc()
