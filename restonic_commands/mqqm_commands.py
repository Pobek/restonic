from restonic_commands import click
from restonic_tools import tools
import requests
import json
from config import Config

config = Config()

@click.command()
@click.option('--state', type=click.Choice(['enabled','disabled']), default="enabled", help='Set the state of the object', show_default=True)
@click.option('--dp-target', help="Set the target of the command. Could either be a single datapower, a list of datapowers. ")
@click.option('--env-target', help="Set the target of the command. Could either be a single datapower environment, a list of datapower environments. ")
@click.argument('qm-name')
@click.argument('queue-manager-ip')
@click.argument('queue-manager-port')
@click.argument('queue-manager-name')
@click.argument('domain_name')
def create_mq_qm(qm_name, queue_manager_ip, queue_manager_port, queue_manager_name, domain_name, state, dp_target, env_target):
    """ This command creates an IBM MQ QueueManager Object """
    click.secho("Creating QM Object : {0}".format(qm_name), fg='yellow')
    
    dp_object = tools.load_datapower_object(config, dp_target, env_target) 

    mqqm_object = {
        "MQQM" : {
            "name" : str(qm_name),
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
        if int(int(response.status_code) / 100) == 2:
            click.secho('Success - QM {0} has been created!.'.format(qm_name), fg='green')
            return True
        else:
            click.secho('Failure - QM {0} could not been created! error: {1}.'.format(qm_name, response.json()['error']), fg='red')
    elif isinstance(dp_object, list):
        for datapower in dp_object:
            auth = (datapower["credentials"]["username"], datapower["credentials"]["password"])
            link = str(datapower["datapower_rest_url"]) + "config/"+ str(domain_name) +"/MQQM"
            response = requests.post(url=link, data=json.dumps(mqqm_object), auth=auth, verify=False)
            if int(int(response.status_code) / 100) == 2:
                click.secho('Datapower {0} : Success - QM {1} has been created!'.format(datapower["name"], qm_name), fg='green')
                return True
            else:
                click.secho('Datapower {0} : Failure - QM {1} could not been created ! error: {2}.'.format(datapower["name"], qm_name, response.json()['error']), fg='red')
    return False