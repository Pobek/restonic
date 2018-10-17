from cli import click
import requests
import json
from config import Config

config = Config().config
auth = (config["credentials"]["username"], config["credentials"]["password"])

@click.command()
def create_policy():
    """ This command creates a Policy Object """
    click.secho("Creating Policy", fg='yellow')