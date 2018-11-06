from restonic_commands import click
import requests
import json
import urllib3
from config import Config

config = Config()

@click.command()
@click.option('--state', type=click.Choice(['enabled', 'disabled']), default="enabled", help='Set the state of the object', show_default=True)
@click.option('--dp-target', help="Set the target of the command. Could either be a single datapower, a list of datapowers. ")
@click.option('--env-target', help="Set the target of the command. Could either be a single datapower environment, a list of datapower environments. ")
@click.argument('name')
@click.argument('listen_address')
@click.argument('listen_port')
@click.argument('domain_name')
def create_http_fsh(name, listen_address, listen_port, domain_name, state, dp_target, env_target):
    """ This command creates an HTTP Front side handler """
    click.echo("Creating a new HTTP FSH : {0}".format(name))

    dp_object = None

    if (not dp_target is None and not env_target is None) or (dp_target is None and not env_target is None):
        dp_object = config.config[env_target]
    elif not dp_target is None and env_target is None:
        dp_object = config.get_dp_object_from_dp_name(dp_target)
    else:
        click.secho("The option '--dp-target' or '--env-target' must be initialized to use this command.", fg='red') 
        return
    
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

    if isinstance(dp_object, dict):
        auth = (dp_object["credentials"]["username"], dp_object["credentials"]["password"])
        link = str(dp_object["datapower_rest_url"]) + "config/"+ str(domain_name) +"/HTTPSourceProtocolHandler"
        response = requests.post(url=link, data=json.dumps(http_fsh_object), auth=auth, verify=False)
        click.echo("{0} -- {1}".format(response.status_code, response.reason))
    elif isinstance(dp_object, list):
        for datapower in dp_object:
            auth = (datapower["credentials"]["username"], datapower["credentials"]["password"])
            link = str(datapower["datapower_rest_url"]) + "config/"+ str(domain_name) +"/HTTPSourceProtocolHandler"
            response = requests.post(url=link, data=json.dumps(http_fsh_object), auth=auth, verify=False)
            click.echo("datapower : {0}, {1} -- {2}".format(datapower["name"], response.status_code, response.reason))

@click.command()
@click.option('--state', type=click.Choice(['enabled','disabled']), default="enabled", help='Set the state of the object', show_default=True)
@click.option('--dp-target', help="Set the target of the command. Could either be a single datapower, a list of datapowers. ")
@click.option('--env-target', help="Set the target of the command. Could either be a single datapower environment, a list of datapower environments. ")
@click.option('--parse-properties', type=click.Choice(['on','off']), default="on", help='Set whether to parse MQ-Headers or not')
@click.option('--async-put', type=click.Choice(['on','off']), default="on", help='Set wether to use AsyncPut or not')
@click.argument('name')
@click.argument('queue_manager')
@click.argument('queue_name')
@click.argument('domain_name')
def create_mq_fsh(name, queue_manager, queue_name, domain_name, state, dp_target, env_target, parse_properties, async_put):
    """ This command creates an IBM MQ Front sider handler """
    click.echo("Creating a new MQ FSH : {0}".format(name))

    dp_object = None

    if (not dp_target is None and not env_target is None) or (dp_target is None and not env_target is None):
        dp_object = config.config[env_target]
    elif not dp_target is None and env_target is None:
        dp_object = config.get_dp_object_from_dp_name(dp_target)
    else:
        click.secho("The option '--dp-target' or '--env-target' must be initialized to use this command.", fg='red') 
        return

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

    if isinstance(dp_object, dict):
        auth = (dp_object["credentials"]["username"], dp_object["credentials"]["password"])
        link = str(dp_object["datapower_rest_url"]) + "config/"+ str(domain_name) +"/MQSourceProtocolHandler"
        response = requests.post(url=link, data=json.dumps(mq_fsh_object), auth=auth, verify=False)
        click.echo("{0} -- {1}".format(response.status_code, response.reason))
    elif isinstance(dp_object, list):
        for datapower in dp_object:
            auth = (datapower["credentials"]["username"], datapower["credentials"]["password"])
            link = str(datapower["datapower_rest_url"]) + "config/"+ str(domain_name) +"/MQSourceProtocolHandler"
            response = requests.post(url=link, data=json.dumps(mq_fsh_object), auth=auth, verify=False)
            click.echo("datapower : {0}, {1} -- {2}".format(datapower["name"], response.status_code, response.reason))