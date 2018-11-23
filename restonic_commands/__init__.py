import urllib3
from . import click
from .mpgw_commands import list_mpgw, create_mpgw, export_mpgw
from .fsh_commands import create_http_fsh, create_mq_fsh, export_http_fsh
from .mqqm_commands import create_mq_qm
from .generic_utils_commands import save_config
from .policy_commands import create_policy
from .filestore_commands import list_directory

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@click.group()
def restonic():
    pass

# list Commands
restonic.add_command(list_mpgw)
restonic.add_command(list_directory)

# export Commands
restonic.add_command(export_mpgw)
restonic.add_command(export_http_fsh)

# create Commands
restonic.add_command(create_mpgw)
restonic.add_command(create_http_fsh)
restonic.add_command(create_mq_fsh)
restonic.add_command(create_mq_qm)
restonic.add_command(create_policy)

# general Commands
restonic.add_command(save_config)