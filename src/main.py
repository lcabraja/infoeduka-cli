import click
from session import verify_credentials, authenticate, reauthenticate

from log import Logger
from endpoints.schedule import schedule_main
from endpoints.materials import materials_main
from credentials import get_login_method, get_credentials, set_credentials, reset_credentials, get_username

logger = None

@click.group(invoke_without_command=False)
@click.option('-t', '--token', help="PHPSESSID token")
@click.option('-u', '--username', help="Your infoeduka username (without @racunarstvo.hr)")
@click.option('-p', '--password', help="Your infoeduka password")
@click.option('-e', '--incognito/--save-credentials', default=False, help="Doesn't save anything to disk")
@click.option('--verbose', default=False, help="Logs additional data")
@click.pass_context
def cli(ctx, token, username, password, incognito, verbose):
    logger = Logger(verbose)
    login_method, token = get_login_method(token, username, password)

    # Check to see if the CLI has any valid credentials
    if login_method == False and ctx.invoked_subcommand not in ["login", "logout"]:
        raise click.ClickException("Missing login credentials! You must log in or provide them via options.")

    # Log in with token provided in options
    if login_method == "token":
        username = "token"

    # Log in with username and password provided in options
    if login_method == "username_password":
        token = authenticate(username, password)
        if not incognito:
            set_credentials(username=username, password=password, token=token)
    
    # Log in with stored credentials
    if login_method == "stored_credentials":
        username = get_username()
        token = reauthenticate()
        logger.debug(f"Loged in to stored user [{get_username()}]")

    ctx.ensure_object(dict)
    ctx.obj['incognito'] = incognito
    ctx.obj['username'] = username
    ctx.obj['method'] = login_method
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
def logout():
    credentials = get_credentials()
    if get_login_method(None, username=credentials["username"], password=credentials["password"]):
        reset_credentials(username=True, password=True, token=True)
        click.echo(f"Logging out from user [{credentials['username']}]")
    else:
        click.echo("No stored credentials found...")


@cli.command()
@click.pass_context
def whoami(ctx):
    answer = "[incognito] " if ctx.obj["incognito"] and ctx.obj["method"] in ["username_password", "token"] else "Logged in "
    if ctx.obj["method"] == "token": answer += f"with token [{ctx.obj['token']}]"
    if ctx.obj["method"] == "username_password": answer += f"as user [{ctx.obj['username']}]"
    if ctx.obj["method"] == "stored_credentials": answer += f"as stored user [{ctx.obj['username']}]"
    click.echo(answer)


@cli.command()
@click.pass_context
def test(ctx):
    click.echo("Test command ran successfully!")

@cli.command()
@click.pass_context
def materials(ctx):
    materials_main(ctx.obj["token"])

@cli.command()
@click.pass_context
def schedule(ctx):
    schedule_main(ctx.obj["token"])

if __name__ == '__main__':
    cli(obj={})
