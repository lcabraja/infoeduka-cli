import click
import json
from credentials import can_continue, get_credentials, set_credentials

@click.group()
@click.option('-t', '--token', help="PHPSESSID token")
@click.option('-u', '--username')
@click.option('-p', '--password')
@click.option('-e','--incognito/--save-credentials', default=False, help="Doesn't save anything to disk")
@click.pass_context
def cli(ctx, token, username, password, incognito):
    login_method = can_continue(token, username, password)
    ctx.ensure_object(dict)
    ctx.obj['login_method'] = login_method
    # TODO: If the following command is NOT login, raise click.ClickException
    # if not login_method: raise click.ClickException("No login credentials found! Try typing:\n$ infoeduka-cli login")

@cli.command()
@click.argument('username')
@click.argument('password')
@click.pass_context
def login(ctx, username, password):
    if can_continue(None, username, password):
        set_credentials(username=username, password=password)

if __name__ == '__main__':
    cli(obj={})
