import click
import requests
import json
import urllib3
from config import Config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
config = Config().config
auth = (config["credentials"]["username"], config["credentials"]["password"])

@click.command()
@click.option('--domain', required=True, help='The working domain')
@click.option('--state', type=click.Choice(['enabled','disabled']), default="enabled", help='Set the state of the object', show_default=True)
@click.argument('object-name')
@click.argument('queue-manager-ip')
@click.argument('queue-manager-port')
@click.argument('queue-manager-name')
def create_mq_qm(object_name, queue_manager_ip, queue_manager_port, queue_manager_name, domain, state):
    """ This command creates an IBM MQ QueueManager Object """
    click.echo("Creating QM Object : {0}".format(object_name))
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
    link = str(config["datapower_rest_url"]) + "config/"+ str(domain) +"/MQQM"
    response = requests.post(url=link, data=json.dumps(mqqm_object), auth=auth, verify=False)
    click.echo("{0} -- {1}".format(response.status_code, response.reason))