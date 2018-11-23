import time
import requests

def load_datapower_object(config_ref, dp_target_ref, env_target_ref):
    if (not dp_target_ref is None and not env_target_ref is None) or (dp_target_ref is None and not env_target_ref is None):
        return config_ref.config[env_target_ref]
    elif not dp_target_ref is None and env_target_ref is None:
        return config_ref.get_dp_object_from_dp_name(dp_target_ref)
    raise Exception("The option '--dp-target' or '--env-target' must be initialized to use this command.")

def get_exported_json_object(dp_conf, action_response, auth):
    if int(int(action_response.status_code) / 100) == 2:
        exported_object_location_url = str(dp_conf["datapower_rest_url"]) + str(action_response.json()["_links"]["location"]["href"])[6:]
        time.sleep(1)
        exported_object_json_response = requests.get(url=exported_object_location_url, auth=auth, verify=False).json()
        return exported_object_json_response["result"] if not('error' in exported_object_json_response) else None
    return None