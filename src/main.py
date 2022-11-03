import click
from credentials import can_continue, get_credentials, set_credentials, reset_credentials
from session import verify_credentials, authenticate, reauthenticate
from log import Loggeer

logger = None

@click.group(invoke_without_command=False)
@click.option('-t', '--token', help="PHPSESSID token")
@click.option('-u', '--username', help="Your infoeduka username (without @racunarstvo.hr)")
@click.option('-p', '--password', help="Your infoeduka password")
@click.option('-e', '--incognito/--save-credentials', default=False, help="Doesn't save anything to disk")
@click.option('--verbose', default=False, help="Logs additional data")
@click.pass_context
def cli(ctx, token, username, password, incognito, verbose):
    logger = Loggeer(verbose)
    login_method, login_credentials = can_continue(token, username, password)
    
    if login_method == False and ctx.invoked_subcommand not in ["login", "logout"]:
        raise click.ClickException(
            "Missing login credentials! You must log in or provide them via options.")

    token = ""

    if login_method == "username+password":
        token = authenticate(username, password)
        if username and password and not incognito:
            set_credentials(username=username, password=password, token=token)
    
    if login_method == "token":
        token = login_credentials
    
    if login_method == "stored_credentials":
        credentials = reauthenticate()
        if credentials:
            token = credentials["phpsessid"]
        else:
            click.echo("")

    ctx.ensure_object(dict)
    ctx.obj['token'] = token


@cli.command()
@click.argument('username')
@click.argument('password')
@click.option('-v', '--verify/--bold', default=True, help="Verifies account by logging in")
@click.pass_context
def login(ctx, username, password, verify):
        if verify: 
            token = verify_credentials(username, password)
            if not token:
                click.echo("Invalid credentials!")
                raise click.Abort()
            set_credentials(token=token)
        set_credentials(username=username, password=password)



@cli.command()
@click.pass_context
def logout(ctx):
    credentials = get_credentials()
    if can_continue(None, username=credentials["username"], password=credentials["password"]):
        reset_credentials(username=True, password=True, token=True)
        click.echo(f"Logging out from user [{credentials['username']}]")
    else:
        click.echo("No stored credentials found...")


@cli.command()
@click.pass_context
def test(ctx):
    click.echo("Test command ran successfully!")


if __name__ == '__main__':
    cli(obj={})
