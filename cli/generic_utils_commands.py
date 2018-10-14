import click
import requests
import json
import urllib3
from config import Config

config = Config().config
auth = (config["credentials"]["username"], config["credentials"]["password"])

@click.command()
@click.argument('domain_name')
def save_config(domain_name):
    """ This command creates an IBM MQ Front sider handler """
    click.secho("Saving Configuration", fg='yellow')
    config_object = {
        "SaveConfig" : ""
    }
    link = str(config["datapower_rest_url"]) + "actionqueue/"+ str(domain_name)
    response = requests.post(url=link, data=json.dumps(config_object), auth=auth, verify=False)
    click.echo("{0} -- {1}".format(response.status_code, response.reason))
    if int(int(response.status_code) / 100) == 2:
        click.secho('Success - Configuration saved.', fg='green')
    else:
        click.secho('Failure - Configuration not saved.', fg='red')