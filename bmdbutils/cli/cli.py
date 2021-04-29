"""
CLI entry point.
"""

import click

from .commands.upload import upload


@click.group()
def main():
    pass


main.add_command(upload)
