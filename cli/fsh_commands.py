import click
from config import Config

@click.command()
def create_http_fsh():
    """ This command creates an HTTP Front side handler """
    click.echo("Creating http fsh")

@click.command()
def create_mq_fsh():
    """ This command creates an IBM MQ Front sider handler """
    click.echo("Creating mq fsh")