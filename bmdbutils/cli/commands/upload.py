"""
$ bmbdutils upload
"""
import click


@click.command(
    short_help="Uploads a table with models, records or species to a "
               "MongoDB collection."
)
def upload():
    pass
