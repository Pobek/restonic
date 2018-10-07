import click

from .mpgw_commands import create_mpgw
from .fsh_commands import create_http_fsh, create_mq_fsh 

@click.group()
def cli():
    pass

cli.add_command(create_mpgw)
cli.add_command(create_http_fsh)
cli.add_command(create_mq_fsh)