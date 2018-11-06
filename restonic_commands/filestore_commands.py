from restonic_commands import click
import requests
import json
import urllib3
import codecs
from config import Config

config = Config()

@click.command()
@click.option('--dp-target', help="Set the target of the command. Could either be a single datapower, a list of datapowers. ")
@click.option('--env-target', help="Set the target of the command. Could either be a single datapower environment, a list of datapower environments. ")
@click.option('--file-target', help="Save the response content in a file")
@click.argument('target_directory', help="The target directory. Needs to be in the format : '<dp_dir>/<target_dir>' or just '<dp_dir>/'")
@click.argument('domain_name')
def list_directory(target_directory, domain_name, dp_target, env_target, file_target):
    """ This command lets you manipulate files from the datapower """

    dp_object = None

    if (not dp_target is None and not env_target is None) or (dp_target is None and not env_target is None):
        dp_object = config.config[env_target]
    elif not dp_target is None and env_target is None:
        dp_object = config.get_dp_object_from_dp_name(dp_target)
    else:
        click.secho("The option '--dp-target' or '--env-target' must be initialized to use this command.", fg='red') 
        return

    if isinstance(dp_object, dict):
        click.secho("Searching for directory '{0}'".format(target_directory))
        auth = (dp_object["credentials"]["username"], dp_object["credentials"]["password"])
        folder_split = target_directory.split("/")
        if len(folder_split) > 1:
            link = str(dp_object["datapower_rest_url"]) + "filestore/"+ str(domain_name) +"/"+ str(target_directory)
        else:
            link = str(dp_object["datapower_rest_url"]) + "filestore/"+ str(domain_name) +"/"+ str(target_directory)
        click.echo(link)
        response = requests.get(url=link, auth=auth, verify=False)
        response_json = response.json()["filestore"]["location"]
        click.echo("{0} -- {1}".format(response.status_code, response.reason))
        if not file_target is None:
            with codecs.open(file_target, 'w', 'utf-8') as w_file:
                json.dump(response_json, w_file, sort_keys=True, indent=4, ensure_ascii=False)
            click.secho("Response saved to : '{0}'".format(file_target), fg="green")
        else:
            click.echo("Content : {0}".format(json.dumps(response_json, sort_keys=True, indent=4)))
    elif isinstance(dp_object, list):
        for datapower in dp_object:
            click.secho("Searching for directory '{0}' in datapower : {1}".format(target_directory, datapower["name"]))
            auth = (datapower["credentials"]["username"], datapower["credentials"]["password"])
            folder_split = target_directory.split("/")
            if len(folder_split) > 1:
                link = str(datapower["datapower_rest_url"]) + "filestore/"+ str(domain_name) +"/"+ str(target_directory)
            else:
                link = str(datapower["datapower_rest_url"]) + "filestore/"+ str(domain_name) +"/"+ str(target_directory)
            click.echo(link)
            response = requests.get(url=link, auth=auth, verify=False)
            response_json = response.json()["filestore"]["location"]
            click.echo("{0} -- {1}".format(response.status_code, response.reason))
            if not file_target is None:
                with codecs.open(file_target + "_" + datapower["name"], 'w', 'utf-8') as w_file:
                    json.dump(response_json, w_file, sort_keys=True, indent=4, ensure_ascii=False)
                click.secho("Response saved to : '{0}'".format(file_target), fg="green")
            else:
                click.echo("Datapower {0}, Content : {1}".format(datapower["name"],json.dumps(response_json, sort_keys=True, indent=4)))