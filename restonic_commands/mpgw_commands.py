from restonic_commands import click
from restonic_tools import tools
import requests
import json
import codecs
import os
from config import Config

config = Config()

request_respone_list = ['preprocessed', 'unprocessed', 'xml', 'json', 'soap']
export_types = ["json", "xml", "zip"]

@click.command()
@click.option('--dp-target', help="Set the target of the command. Could either be a single datapower, a list of datapowers. ")
@click.option('--env-target', help="Set the target of the command. Could either be a single datapower environment, a list of datapower environments. ")
@click.option('--path', help="A path to where to save the output.")
@click.argument('domain-name', help="The domain name that the object will be created at")
def list_mpgw(domain_name, dp_target, env_target, path):
    """
        This command retrieves a list of MultiProtocol Gateways from a given target.
    """
    
    dp_object = tools.load_datapower_object(config, dp_target, env_target)

    if isinstance(dp_object, dict):
        auth = (dp_object["credentials"]["username"], dp_object["credentials"]["password"])
        link = str(dp_object["datapower_rest_url"]) + "config/"+ str(domain_name) +"/MultiProtocolGateway"
        mpgw_list_response = requests.get(url=link, auth=auth, verify=False)
        if int(int(mpgw_list_response.status_code) / 100) == 2:
            click.secho('Successfully retrieved a list of MultiProtocol Gateways', fg='green')
            mpgw_list_json = mpgw_list_response.json()["MultiProtocolGateway"]
            mpgw_list = []
            if isinstance(mpgw_list_json, dict):
                mpgw_list.append(mpgw_list_json["name"])
            elif isinstance(mpgw_list_json, list):
                for mpgw in mpgw_list_json:
                    mpgw_list.append(mpgw["name"])
            if path != None:
                file_name = os.path.join(path, "mpgw_list.json")
                click.secho("Saving output to '{0}' : ".format(file_name), fg='green')
                with codecs.open(file_name, "w", "utf-8") as w_file:
                    json.dump(mpgw_list, w_file, sort_keys=True, indent=4, ensure_ascii=False)
            else:
                click.echo(str(mpgw_list))
            return True
        else:
            click.secho('Failure. error: {0}.'.format(mpgw_list_response.json()['error']), fg='red')
    elif isinstance(dp_object, list):
        for datapower in dp_object:
            auth = (datapower["credentials"]["username"], datapower["credentials"]["password"])
            link = str(datapower["datapower_rest_url"]) + "config/"+ str(domain_name) +"/MultiProtocolGateway"
            mpgw_list_response = requests.get(url=link, auth=auth, verify=False)
            if int(int(mpgw_list_response.status_code) / 100) == 2:
                click.secho('Datapower {0} : Successfully retrieved a list of MPGW and their state : '.format(datapower["name"]), fg='green')
                mpgw_list_json = mpgw_list_response.json()["MultiProtocolGateway"]
                mpgw_list = []
                if isinstance(mpgw_list_json, dict):
                    mpgw_list.append(mpgw_list_json["name"])
                elif isinstance(mpgw_list_json, list):
                    for mpgw in mpgw_list_json:
                        mpgw_list.append(mpgw["name"])
                if path != None:
                    file_name = os.path.join(path, datapower["name"] + "_mpgw_list.json")
                    click.secho("Saving output to '{0}' : ".format(file_name), fg='green')
                    with codecs.open(file_name, "w", "utf-8") as w_file:
                        json.dump(mpgw_list, w_file, sort_keys=True, indent=4, ensure_ascii=False)
                else:
                    click.echo(str(mpgw_list))
                return True
            else:
                click.secho('Datapower {0} : Failure. error: {1}.'.format(datapower["name"], mpgw_list_response.json()['error']), fg='red')    
    return False

@click.command()
@click.option('--state', type=click.Choice(['enabled','disabled']), default="enabled", help='Set the state of the object', show_default=True)
@click.option('--dp-target', help="Set the target of the command. Could either be a single datapower, a list of datapowers. ")
@click.option('--env-target', help="Set the target of the command. Could either be a single datapower environment, a list of datapower environments. ")
@click.option('--xml-manager', default='default', help='Set a different xml-manager', show_default=True)
@click.option('--host-rewrite', type=click.Choice(['on','off']), default='on', help="Set whether to let dp rewrite the 'host' header or not", show_default=True)
@click.option('--propagate-uri', type=click.Choice(['on','off']), default='on', help="Set whether to pass on the URI from the client to the destination", show_default=True)
@click.option('--backend-url', default='http://localhost:8080', help='The destination URL. Needs to be in the format of <protocol>://<url>/<uri>', show_default=True)
@click.option('--backend-type', type=click.Choice(['static','dynamic']), default='static', help="Sets either to be a 'static' backend or 'dynamic' backend. 'static' is a single end-point while 'dynamic' is multiple end-points predetermined in the policy", show_default=True)
@click.argument('mpgw-name', help='The name of the MultiProtocol Gateway')
@click.argument('fsh-name', help='Either a list or a single name of Front-Side Handlers to add as a refence to the created MPGW')
@click.argument('request-type', help="The type of the request being sent to the mpgw. must contain a value out of this list :[\'preprocessed\', \'unprocessed\', \'xml\', \'json\', \'soap\']")
@click.argument('response-type', help="The type of the response being sent from the mpgw. must contain a value out of this list :[\'preprocessed\', \'unprocessed\', \'xml\', \'json\', \'soap\']")
@click.argument('policy-name', help="The name of the Policy to be attached to this MPGW (Must be an existing Policy)")
@click.argument('domain-name', help="The domain name that the object will be created at")
def create_mpgw(mpgw_name, fsh_name, backend_url, backend_type, request_type, response_type, policy_name, domain_name, state, dp_target, env_target, xml_manager, host_rewrite, propagate_uri):
    """ This command creates a Multi-Protocol-Gateway
        
        Note: The 'backend_type' is an option but it is highly recommended to set a type. In case the 'backend_type' is 'static', use the option 'backend_url' as well or else the default value will be applied instead.
    """

    if not any(request_type.lower() in req for req in request_respone_list):
        click.secho("The request type is not among the permitted types. Use --help to view possible types.", fg='red')
        return
    elif not any(response_type.lower() in res for res in request_respone_list):
        click.secho("The response type is not among the permitted types. Use --help to view possible types.", fg='red')
        return

    dp_object = tools.load_datapower_object(config, dp_target, env_target) 

    click.secho("Creating MPGW : {0}".format(mpgw_name), fg='yellow')

    mpgw_object = {
        "MultiProtocolGateway": {
            "name": str(mpgw_name), # Name of the mpgw *required*
            "mAdminState": str(state), # The state (default enabled) *required*
            "FrontProtocol": { # The FSH list (either [] or {}) *required*
                "value" : str(fsh_name)
            }, 
            "XMLManager": str(xml_manager), # The xml-manager (default default) *required*
            "BackendUrl": str(backend_url), # The backendUrl *required*
            "PropagateURI": str(propagate_uri), # Whether to propagate-url or not (default on) *required*
            "PersistentConnections": "on",
            "LoopDetection": "off",
            "DoHostRewriting": str(host_rewrite), # Should datapower rewrite the 'host' header (default on)
            "DoChunkedUpload": "off",
            "ProcessHTTPErrors": "on",
            "HTTPClientIPLabel": "X-Client-IP",
            "HTTPLogCorIDLabel": "X-Global-Transaction-ID",
            "InOrderMode": {
                "Request": "off",
                "Backend": "off",
                "Response": "off"
            },
            "ForcePolicyExec": "off",
            "RewriteErrors": "on",
            "DelayErrors": "on",
            "DelayErrorsDuration": 1000,
            "RequestType": str(request_type), # The request type (preprocessed = non-xml) *required*
            "ResponseType": str(response_type), # The respone type (preprocessed = non-xml) *required*
            "FollowRedirects": "on",
            "RewriteLocationHeader": "off",
            "StylePolicy": str(policy_name), # The policy name *required*
            "Type": "{0}-backend".format(str(backend_type)), # The type of the backend (default static-backend) *required*
            "AllowCompression": "off",
            "AllowCacheControlHeader": "off",
            "PolicyAttachments": "Test", # ?
            "WSMAgentMonitor": "off",
            "WSMAgentMonitorPCM": "all-messages",
            "ProxyHTTPResponse": "off",
            "TransactionTimeout": 0
        }
    }

    if isinstance(dp_object, dict):
        auth = (dp_object["credentials"]["username"], dp_object["credentials"]["password"])
        link = str(dp_object["datapower_rest_url"]) + "config/"+ str(domain_name) +"/MultiProtocolGateway"
        response = requests.post(url=link, data=json.dumps(mpgw_object), auth=auth, verify=False)
        if int(int(response.status_code) / 100) == 2:
            click.secho('Success - MPGW {0} has been created!.'.format(mpgw_name), fg='green')
            return True
        else:
            click.secho('Failure - MPGW {0} could not been created! error: {1}.'.format(mpgw_name, response.json()['error']), fg='red')
    elif isinstance(dp_object, list):
        for datapower in dp_object:
            auth = (datapower["credentials"]["username"], datapower["credentials"]["password"])
            link = str(datapower["datapower_rest_url"]) + "config/"+ str(domain_name) +"/MultiProtocolGateway"
            response = requests.post(url=link, data=json.dumps(mpgw_object), auth=auth, verify=False)
            if int(int(response.status_code) / 100) == 2:
                click.secho('Datapower {0} : Success - MPGW {1} has been created!'.format(datapower["name"], mpgw_name), fg='green')
                return True
            else:
                click.secho('Datapower {0} : Failure - MPGW {1} could not been created ! error: {2}.'.format(datapower["name"], mpgw_name, response.json()['error']), fg='red')
    return False

@click.command()
@click.option('--dp-target', help="Set the target of the command. Could either be a single datapower, a list of datapowers. ")
@click.option('--env-target', help="Set the target of the command. Could either be a single datapower environment, a list of datapower environments. ")
@click.option('--all-files', is_flag=True, help="Set whether to export all the files associated with said MultiProtocol Gateway.")
@click.option('--include-internal-files', is_flag=True, help="Set whether to export all internal files associated with said MultiProtocol Gateway.")
@click.argument('mpgw-target', help="Said MultiProtocol Gateway to be exported.")
@click.argument('export-type', help="Which file type save the exported object as.")
@click.argument('directory-path', help="A path to a directory that will hold the exported content.")
@click.argument('domain-name', help="The domain name that said MultiProtocol Gateway exists.")
def export_mpgw(domain_name, mpgw_target, export_type, directory_path, dp_target, env_target, all_files, include_internal_files):
    """ This command lets you export said MultiProtocol Gateway as either
    one of these options: JSON | XML | ZIP """
    if not any(export_type.lower() in export for export in export_types):
        click.secho("The export type is not among the permitted types. Use --help to view possible types.", fg='red')
        return

    dp_object = tools.load_datapower_object(config, dp_target, env_target) 

    click.secho("Exporting MultiProtocol Gateway : '{0}' to '{1}' as a {2} file...".format(mpgw_target, directory_path, export_type.title()), fg='yellow')

    export_request_object = {
        "Export" : {
            "Format" : str(export_type).upper(),
            "AllFiles" : str("on" if all_files else "off"),
            "IncludeInternalFiles" : str("on" if include_internal_files else "off"),
            "Object" : {
                "class" : "MultiProtocolGateway",
                "name" : str(mpgw_target),
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
            file_name = os.path.join(directory_path, str(mpgw_target + "_MPGW_Export.json"))
            with codecs.open(file_name, "w", "utf-8") as w_file:
                json.dump(export_response, w_file, sort_keys=True, indent=4, ensure_ascii=False)
            click.secho("Success - Exported '{0}' to '{1}'.".format(mpgw_target, file_name), fg='green')
            return True
        else:
            click.secho("Failure - Could'nt export '{0}'.".format(mpgw_target), fg='red')
    elif isinstance(dp_object, list):
        for datapower in dp_object:
            auth = (datapower["credentials"]["username"], datapower["credentials"]["password"])
            link = str(datapower["datapower_rest_url"]) + "actionqueue/"+ str(domain_name)
            action_response = requests.post(url=link, data=json.dumps(export_request_object), auth=auth, verify=False)
            export_response = tools.get_exported_json_object(datapower, action_response, auth)
            if export_response != None:
                file_name = os.path.join(directory_path, str(mpgw_target + "_MPGW_Export_" + datapower["name"] + ".json"))
                with codecs.open(file_name, "w", "utf-8") as w_file:
                    json.dump(export_response, w_file, sort_keys=True, indent=4, ensure_ascii=False)
                click.secho("Datapower {0} : Success - Exported '{1}' to '{2}'.".format(datapower["name"], mpgw_target, file_name), fg='green')
                return True
            else:
                click.secho("Datapower {0} : Failure - Could'nt export '{1}'.".format(datapower["name"], mpgw_target), fg='red')
    return False