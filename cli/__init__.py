import urllib3
from . import click
#from .mpgw_commands import create_mpgw
from .fsh_commands import create_http_fsh, create_mq_fsh 
#from .mqqm_commands import create_mq_qm
#from .generic_utils_commands import save_config
#from .policy_commands import create_policy

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@click.group()
def restonic():
    pass

#restonic.add_command(create_mpgw)
restonic.add_command(create_http_fsh)
#restonic.add_command(create_mq_fsh)
#restonic.add_command(create_mq_qm)
#restonic.add_command(save_config)
#restonic.add_command(create_policy)