import click
import requests
import json
import urllib3
from config import Config

config = Config().config
auth = (config["credentials"]["username"], config["credentials"]["password"])

@click.command()
def create_mpgw():
    """ This command creates a Multi-Protocol-Gateway """
    click.echo("Creating mpgw")