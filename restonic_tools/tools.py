def load_datapower_object(config_ref, dp_target_ref, env_target_ref):
    if (not dp_target_ref is None and not env_target_ref is None) or (dp_target_ref is None and not env_target_ref is None):
        return config_ref.config[env_target_ref]
    elif not dp_target_ref is None and env_target_ref is None:
        return config_ref.get_dp_object_from_dp_name(dp_target_ref)
    raise Exception("The option '--dp-target' or '--env-target' must be initialized to use this command.")