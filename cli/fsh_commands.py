import click
import requests
import json
import urllib3
from config import Config

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@click.command()
@click.option('--domain', required=True, help='The working domain')
@click.option('--file', default=None, help='Path to file containing the object values')
@click.option('--state', type=click.Choice(['enabled','disabled']), default="enabled", help='Set the state of the object', show_default=True)
@click.argument('name')
@click.argument('listen_address')
@click.argument('listen_port')
def create_http_fsh(name, listen_address, listen_port, domain, file, state):
    """ This command creates an HTTP Front side handler """
    click.echo("Creating a new HTTP FSH : {0}".format(name))
    config = Config().config
    http_fsh_object = {
        "HTTPSourceProtocolHandler" : {
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
            "PersistentConnections" : "on",
            "mAdminState" : str(state),
            "name" : str(name)
        }
    }
    link = str(config["datapower_rest_url"]) + "config/"+ str(domain) +"/HTTPSourceProtocolHandler"
    auth = (config["credentials"]["username"], config["credentials"]["password"])
    response = requests.post(url=link, data=json.dumps(http_fsh_object), auth=auth, verify=False)
    click.echo("{0} -- {1}".format(response.status_code, response.reason))

@click.command()
def create_mq_fsh():
    """ This command creates an IBM MQ Front sider handler """
    click.echo("Creating mq fsh")