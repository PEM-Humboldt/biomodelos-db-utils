"""
bmdbutils CLI entry point.
"""

import click

from .commands.upload import upload
from .commands.geoserver.geoserver import geoserver


@click.group()
def main():
    pass


main.add_command(upload)
main.add_command(geoserver)
