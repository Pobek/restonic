import click
from .mpgw_commands import create_mpgw
from .fsh_commands import create_http_fsh, create_mq_fsh 
from .mqqm_commands import create_mq_qm

@click.group()
def restonic():
    pass

restonic.add_command(create_mpgw)
restonic.add_command(create_http_fsh)
restonic.add_command(create_mq_fsh)
restonic.add_command(create_mq_qm)