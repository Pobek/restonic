from restonic_commands import click
from restonic_tools import tools
import requests
import json
import codecs
import os
from config import Config

config = Config()

export_types = ["json", "xml", "zip"]

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

    dp_object = tools.load_datapower_object(config, dp_target, env_target) 
    
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
@click.option('--dp-target', help="Set the target of the command. Could either be a single datapower, a list of datapowers. ")
@click.option('--env-target', help="Set the target of the command. Could either be a single datapower environment, a list of datapower environments. ")
@click.option('--all-files', is_flag=True, help="Set whether to export all the files associated with said MultiProtocol Gateway.")
@click.option('--include-internal-files', is_flag=True, help="Set whether to export all internal files associated with said MultiProtocol Gateway.")
@click.argument('fsh-target', help="Said MultiProtocol Gateway to be exported.")
@click.argument('export-type', help="Which file type save the exported object as.")
@click.argument('directory-path', help="A path to a directory that will hold the exported content.")
@click.argument('domain-name', help="The domain name that said MultiProtocol Gateway exists.")
def export_http_fsh(domain_name, fsh_target, export_type, directory_path, dp_target, env_target, all_files, include_internal_files):
    """ This command lets you export said HTTP Front Side Handler as either
    one of these options: JSON | XML | ZIP """
    if not any(export_type.lower() in export for export in export_types):
        click.secho("The export type is not among the permitted types. Use --help to view possible types.", fg='red')
        return

    dp_object = tools.load_datapower_object(config, dp_target, env_target) 

    click.secho("Exporting HTTP Front Side Handler : '{0}' to '{1}' as a {2} file...".format(fsh_target, directory_path, export_type.title()), fg='yellow')

    export_request_object = {
        "Export" : {
            "Format" : str(export_type).upper(),
            "AllFiles" : str("on" if all_files else "off"),
            "IncludeInternalFiles" : str("on" if include_internal_files else "off"),
            "Object" : {
                "class" : "HTTPSourceProtocolHandler",
                "name" : str(fsh_target),
                "ref-objects" : "on"
            }
        }
    }

    if isinstance(dp_object, dict):
        auth = (dp_object["credentials"]["username"], dp_object["credentials"]["password"])
        link = str(dp_object["datapower_rest_url"]) + "actionqueue/"+ str(domain_name)
        action_response = requests.post(url=link, data=json.dumps(export_request_object), auth=auth, verify=False)
        export_response = tools.get_exported_json_object(dp_object, action_response, auth)
        if export_response != None:
            file_name = os.path.join(directory_path, str(fsh_target + "_HTTP_FSH_Export.json"))
            with codecs.open(file_name, "w", "utf-8") as w_file:
                json.dump(export_response, w_file, sort_keys=True, indent=4, ensure_ascii=False)
            click.secho("Success - Exported '{0}' to '{1}'.".format(fsh_target, file_name), fg='green')
        else:
            click.secho("Failure - Could'nt export '{0}'.".format(fsh_target), fg='red')
    elif isinstance(dp_object, list):
        for datapower in dp_object:
            auth = (datapower["credentials"]["username"], datapower["credentials"]["password"])
            link = str(datapower["datapower_rest_url"]) + "actionqueue/"+ str(domain_name)
            action_response = requests.post(url=link, data=json.dumps(export_request_object), auth=auth, verify=False)
            export_response = tools.get_exported_json_object(datapower, action_response, auth)
            if export_response != None:
                file_name = os.path.join(directory_path, str(fsh_target + "_HTTP_FSH_Export_" + datapower["name"] + ".json"))
                with codecs.open(file_name, "w", "utf-8") as w_file:
                    json.dump(export_response, w_file, sort_keys=True, indent=4, ensure_ascii=False)
                click.secho("Datapower {0} : Success - Exported '{1}' to '{2}'.".format(datapower["name"], fsh_target, file_name), fg='green')
            else:
                click.secho("Datapower {0} : Failure - Could'nt export '{1}'.".format(datapower["name"], fsh_target), fg='red')

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

    dp_object = tools.load_datapower_object(config, dp_target, env_target) 

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