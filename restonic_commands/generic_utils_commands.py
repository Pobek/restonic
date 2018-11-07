from restonic_commands import click
import requests
import json
import urllib3
from config import Config

config = Config()

@click.command()
@click.option('--dp-target', help="Set the target of the command. Could either be a single datapower, a list of datapowers. ")
@click.option('--env-target', help="Set the target of the command. Could either be a single datapower environment, a list of datapower environments. ")
@click.argument('domain_name')
def save_config(domain_name, dp_target, env_target):
    """ This command creates an IBM MQ Front sider handler """
    click.secho("Saving Configuration", fg='yellow')

    dp_object = tools.load_datapower_object(config, dp_target, env_target) 

    config_object = {
        "SaveConfig" : ""
    }
    
    if isinstance(dp_object, dict):
        auth = (dp_object["credentials"]["username"], dp_object["credentials"]["password"])
        link = str(dp_object["datapower_rest_url"]) + "actionqueue/"+ str(domain_name)
        response = requests.post(url=link, data=json.dumps(config_object), auth=auth, verify=False)
        click.echo("{0} -- {1}".format(response.status_code, response.reason))
        if int(int(response.status_code) / 100) == 2:
            click.secho('Success - Configuration saved.', fg='green')
        else:
            click.secho('Failure - Configuration not saved.', fg='red')
    elif isinstance(dp_object, list):
        for datapower in dp_object:
            auth = (datapower["credentials"]["username"], datapower["credentials"]["password"])
            link = str(datapower["datapower_rest_url"]) + "actionqueue/"+ str(domain_name)
            response = requests.post(url=link, data=json.dumps(config_object), auth=auth, verify=False)
            click.echo("{0} -- {1}".format(response.status_code, response.reason))
            if int(int(response.status_code) / 100) == 2:
                click.secho('Success - Configuration saved for {0}.'.format(datapower["name"]), fg='green')
            else:
                click.secho('Failure - Configuration not saved for {0}.'.format(datapower["name"]), fg='red')