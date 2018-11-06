from restonic_commands import click
import requests
import json
import urllib3
from config import Config

config = Config()

@click.command()
@click.option('--state', type=click.Choice(['enabled','disabled']), default="enabled", help='Set the state of the object', show_default=True)
@click.option('--dp-target', help="Set the target of the command. Could either be a single datapower, a list of datapowers. ")
@click.option('--env-target', help="Set the target of the command. Could either be a single datapower environment, a list of datapower environments. ")
@click.argument('object-name')
@click.argument('queue-manager-ip')
@click.argument('queue-manager-port')
@click.argument('queue-manager-name')
@click.argument('domain_name')
def create_mq_qm(object_name, queue_manager_ip, queue_manager_port, queue_manager_name, domain_name, state, dp_target, env_target):
    """ This command creates an IBM MQ QueueManager Object """
    click.echo("Creating QM Object : {0}".format(object_name))
    
    dp_object = None

    if (not dp_target is None and not env_target is None) or (dp_target is None and not env_target is None):
        dp_object = config.config[env_target]
    elif not dp_target is None and env_target is None:
        dp_object = config.get_dp_object_from_dp_name(dp_target)
    else:
        click.secho("The option '--dp-target' or '--env-target' must be initialized to use this command.", fg='red') 
        return

    mqqm_object = {
        "MQQM" : {
            "name" : str(object_name),
            "mAdminState" : str(state),
            "HostName" : "{0}:{1}".format(queue_manager_ip, queue_manager_port),
            "QMName" : str(queue_manager_name),
            "CCSID" : 819,
            "ChannelName" : "SYSTEM.DEF.SVRCONN",
            "Heartbeat" : 300,
            "MaximumMessageSize" : 1048576,
            "UnitsOfWork" : "",
            "AutomaticBackout" : "off",
            "TotalConnectionLimit" : 250,
            "InitialConnections" : 1,
            "SharingConversations" : 0,
            "ShareSingleConversation" : "off",
            "PermitInsecureServers" : "off",
            "PermitSSLv3" : "off",
            "SSLcipher" : "none",
            "ConvertInput" : "on",
            "AutoRetry" : "on",
            "RetryInterval" : 1,
            "RetryAttempts" : 0,
            "LongRetryInterval" : 1800,
            "ReportingInterval" : 1,
            "AlternateUser" : "on",
            "SSLClientConfigType" : "proxy"
        }

    }
    if isinstance(dp_object, dict):
        auth = (dp_object["credentials"]["username"], dp_object["credentials"]["password"])
        link = str(dp_object["datapower_rest_url"]) + "config/"+ str(domain_name) +"/MQQM"
        response = requests.post(url=link, data=json.dumps(mqqm_object), auth=auth, verify=False)
        click.echo("{0} -- {1}".format(response.status_code, response.reason))
    elif isinstance(dp_object, list):
        for datapower in dp_object:
            auth = (datapower["credentials"]["username"], datapower["credentials"]["password"])
            link = str(datapower["datapower_rest_url"]) + "config/"+ str(domain_name) +"/MQQM"
            response = requests.post(url=link, data=json.dumps(mqqm_object), auth=auth, verify=False)
            click.echo("datapower : {0}, {1} -- {2}".format(datapower["name"],  response.status_code, response.reason))
