import click
from .tools.auth import set_auth, get_auth

@click.group()
def udebug():
    """udebug integration."""
    pass

@udebug.command()
@click.option("--user", prompt=True)
@click.option("--password", prompt=True, hide_input=True)
def auth(**kwargs):
    """Authenticate with udebug."""
    handle_auth(**kwargs)

def handle_auth(user, password):
    set_auth("icanc.udebug", user, password)
    click.echo("Your credentials were stored!")
    click.echo("If you have ", nl=False)
    click.secho("API access ", nl=False, bold=True)
    click.echo("to udebug, you can now use icanc create testcases -u.")
