from restonic_commands import click
import requests
import json
from config import Config

config = Config()

@click.command()
def create_policy():
    """ This command creates a Policy Object """
    click.secho("Creating Policy", fg='yellow')