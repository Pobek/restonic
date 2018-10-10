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
@click.argument('name')
@click.argument('listen_address')
@click.argument('listen_port')
def create_http_fsh(name, listen_address, listen_port, domain, state):
    """ This command creates an HTTP Front side handler """
    click.echo("Creating a new HTTP FSH : {0}".format(name))
    http_fsh_object = {
        "HTTPSourceProtocolHandler" : {
            "name" : str(name),
            "mAdminState" : str(state),
            "AllowedFeatures" : {
                "CONNECT" : "off",
                "CmdExe" : "off",
                "CustomMethods" : "off",
                "DELETE" : "off",
                "DotDot" : "off",
                "FragmentIdentifiers" : "on",
                "GET" : "off",
                "HEAD" : "off",
                "HTTP-1.0" : "on",
                "HTTP-1.1" : "on",
                "OPTIONS" : "off",
                "POST" : "on",
                "PUT" : "on",
                "QueryString" : "on",
                "TRACE" : "off"
            },
            "HTTPVersion" : "HTTP/1.1",
            "LocalAddress" : str(listen_address),
            "LocalPort" : str(listen_port),
            "PersistentConnections" : "on"
        }
    }
    link = str(config["datapower_rest_url"]) + "config/"+ str(domain) +"/HTTPSourceProtocolHandler"
    response = requests.post(url=link, data=json.dumps(http_fsh_object), auth=auth, verify=False)
    click.echo("{0} -- {1}".format(response.status_code, response.reason))

@click.command()
@click.option('--domain', required=True, help='The working domain')
@click.option('--state', type=click.Choice(['enabled','disabled']), default="enabled", help='Set the state of the object', show_default=True)
@click.option('--parse-properties', type=click.Choice(['on','off']), default="on", help='Set whether to parse MQ-Headers or not')
@click.option('--async-put', type=click.Choice(['on','off']), default="on", help='Set wether to use AsyncPut or not')
@click.argument('name')
@click.argument('queue_manager')
@click.argument('queue_name')
def create_mq_fsh(name, queue_manager, queue_name, domain, state, parse_properties, async_put):
    """ This command creates an IBM MQ Front sider handler """
    click.echo("Creating a new MQ FSH : {0}".format(name))
    mq_fsh_object = {
        "MQSourceProtocolHandler" : {
            "name" : str(name),
            "mAdminState" : str(state),
            "QueueManager" : str(queue_manager),
            "GetQueue" : str(queue_name),
            "CodePage" : 1204,
            "GetMessageOptions" : 1,
            "ParseProperties" : str(parse_properties),
            "AsyncPut" : str(async_put),
            "ExcludeHeaders" : {
                "MQCIH" : "off",
                "MQDLH" : "off",
                "MQIIH" : "off",
                "MQRFH" : "off",
                "MQRFH2" : "off",
                "MQWIH" : "off"
            },
            "ConcurrentConnections" : 1,
            "PollingInterval" : 30,
            "BatcjSize" : 0,
            "ContentTypeHeader" : "None",
            "RetrieveBackoutSettings" : "off",
            "UseQMNameInURL" : "off"
        }
    }
    click.echo(mq_fsh_object)
    link = str(config["datapower_rest_url"]) + "config/"+ str(domain) +"/MQSourceProtocolHandler"
    response = requests.post(url=link, data=json.dumps(mq_fsh_object), auth=auth, verify=False)
    click.echo("{0} -- {1}".format(response.status_code, response.reason))
