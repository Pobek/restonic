from cli import click
import requests
import json
from config import Config

config = Config().config
auth = (config["credentials"]["username"], config["credentials"]["password"])

request_respone_list = ['preprocessed', 'unprocessed', 'xml', 'json', 'soap']

@click.command()
@click.option('--state', type=click.Choice(['enabled','disabled']), default="enabled", help='Set the state of the object', show_default=True)
@click.option('--xml-manager', default='default', help='Set a different xml-manager', show_default=True)
@click.option('--host-rewrite', type=click.Choice(['on','off']), default='on', help="Set whether to let dp rewrite the 'host' header or not", show_default=True)
@click.option('--propagate-uri', type=click.Choice(['on','off']), default='on', help="Set whether to pass on the URI from the client to the destination", show_default=True)
@click.argument('mpgw-name')
@click.argument('fsh-name')
@click.argument('backend-url')
@click.argument('request-type')
@click.argument('reponse-type')
def create_mpgw(mpgw_name, fsh_name, backend_url, request_type, response_type, state, xml_manager, host_rewrite, propagate_uri):
    """ This command creates a Multi-Protocol-Gateway 

    """

    #    Arguments:
    #    1) MPGW_NAME    TEXT    "The MultiProtocol Gateway Name"
    #    2) FSH_NAME     TEXT    "A name of an FSH to be added as a reference to this mpgw"
    #    3) BACKEND_URL  TEXT    "The destination URL. Needs to be in the format of <protocol>://<url>/<uri>.
    #                             Example: 'https://localhost:8080/myuri'"
    #    4) REQUEST_TYPE TEXT    "The type of the request being sent to the mpgw. must contain a value from the list below:
    #                             ['preprocessed', 'unprocessed', 'xml', 'json', 'soap'] "
    #    5) RESPONSE_TYPE    TEXT    "The type of the response being sent from the mpgw. must contain a value from the list below:
    #                             ['preprocessed', 'unprocessed', 'xml', 'json', 'soap'] "


    if not any(request_type in req for req in request_respone_list):
        click.secho("The request type is not among the permitted types. Use --help to view possible types.")
    elif not any(response_type in res for res in request_respone_list):
        click.secho("The response type is not among the permitted types. Use --help to view possible types.")
    else:
        click.echo("Creating MPGW : {0}".format(mpgw_name))
        mpgw_object = {
            "MultiProtocolGateway": {
                "name": str(mpgw_name), # Name of the mpgw *required*
                "mAdminState": str(state), # The state (default enabled) *required*
                "FrontProtocol": { # The FSH list (either [] or {}) *required*
                    "value" : str(fsh_name)
                }, 
                "XMLManager": str(xml_manager), # The xml-manager (default default) *required*
                "BackendUrl": str(backend_url), # The backendUrl *required*
                "PropagateURI": str(propagate_uri), # Whether to progagate-url or not (default on) *required*
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
                "RequestType": "preprocessed", # The request type (preprocessed = non-xml) *required*
                "ResponseType": "preprocessed", # The respone type (preprocessed = non-xml) *required*
                "FollowRedirects": "on",
                "RewriteLocationHeader": "off",
                "StylePolicy": "Test_Policy", # The policy name *required*
                "Type": "static-backend", # The type of the backend (default static-backend) *required*
                "AllowCompression": "off",
                "AllowCacheControlHeader": "off",
                "PolicyAttachments": "Test", # ?
                "WSMAgentMonitor": "off",
                "WSMAgentMonitorPCM": "all-messages",
                "ProxyHTTPResponse": "off",
                "TransactionTimeout": 0
            }
        }