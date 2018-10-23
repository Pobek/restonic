from cli import click
import requests
import json
from config import Config

config = Config()

request_respone_list = ['preprocessed', 'unprocessed', 'xml', 'json', 'soap']

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
@click.argument('domain-name')
def create_mpgw(mpgw_name, fsh_name, backend_url, backend_type, request_type, response_type, policy_name, domain_name, state, dp_target, env_target, xml_manager, host_rewrite, propagate_uri):
    """ This command creates a Multi-Protocol-Gateway
        
        Note: The 'backend_type' is an option but it is highly recommended to set a type. In case the 'backend_type' is 'static', use the option 'backend_url' as well or else the default value will be applied instead.
    """

    if not any(request_type in req for req in request_respone_list):
        click.secho("The request type is not among the permitted types. Use --help to view possible types.", fg='red')
        return
    elif not any(response_type in res for res in request_respone_list):
        click.secho("The response type is not among the permitted types. Use --help to view possible types.", fg='red')
        return

    dp_object = None

    if (not dp_target is None and not env_target is None) or (dp_target is None and not env_target is None):
        dp_object = config.config[env_target]
    elif not dp_target is None and env_target is None:
        dp_object = config.get_dp_object_from_dp_name(dp_target)
    else:
        click.secho("The option '--dp-target' or '--env-target' must be initialized to use this command.", fg='red') 
        return

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
        click.echo("{0} -- {1}".format(response.status_code, response.reason))
        if int(int(response.status_code) / 100) == 2:
            click.secho('Success - MPGW {0} has been created!.'.format(mpgw_name), fg='green')
        else:
            click.secho('Failure - MPGW {0} could not been created! error: {1}.'.format(mpgw_name, response.json()['error']), fg='red')
    elif isinstance(dp_object, list):
        for datapower in dp_object:
            auth = (datapower["credentials"]["username"], datapower["credentials"]["password"])
            link = str(datapower["datapower_rest_url"]) + "config/"+ str(domain_name) +"/MultiProtocolGateway"
            response = requests.post(url=link, data=json.dumps(mpgw_object), auth=auth, verify=False)
            click.echo("{0} -- {1}".format(response.status_code, response.reason))
            if int(int(response.status_code) / 100) == 2:
                click.secho('Success - MPGW {0} has been created for {1}!.'.format(mpgw_name, datapower["name"]), fg='green')
            else:
                click.secho('Failure - MPGW {0} could not been created for {1}!. error: {2}.'.format(mpgw_name, datapower["name"], response.json()['error']), fg='red')