import click
from typing import Any


class Loggeer:
    def __init__(self, verbose: bool):
        self.verbose = verbose


    def debug(self, object: Any):
        if self.verbose:
            click.echo(object)

    def info(self, object: Any):
        click.echo(object)
