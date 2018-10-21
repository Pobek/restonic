import os
import sys
import codecs
import json
import click

class Config:
    """ Represents the selected environment configuration
    """

    CONFIG_PATH = os.path.join(os.path.dirname(sys.argv[0]), "configurations")
    if not os.path.exists(CONFIG_PATH):
        os.mkdir(CONFIG_PATH)

    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        try:
            with codecs.open(os.path.join(self.CONFIG_PATH, "config_restonic.json"), "r", "utf-8") as json_file:
                return json.load(json_file) 
        except:
            click.secho("Could not find 'config_restornic.json' configuration. An example one has been created", fg="red")
            self.generate_config()
            return self.load_config()

    def get_environmet_from_dp_name(self, name):
        for key, value in self.config.items():
            if isinstance(value, list):
                for item in value:
                    if item["name"] == name:
                        return value

    def get_dp_object_from_dp_name(self, name):
        for key, value in self.config.items():
            if isinstance(value, list):
                for item in value:
                    if item["name"] == name:
                        return item

    def generate_config(self):
        config_example = {
            "datapower_env_1" : [
                {
                    "name" : "dp1",
                    "comment" : "Datapower dev 1",
                    "credentials" : {
                        "username" : "admin",
                        "password" : "admin"
                    },
                    "datapower_rest_url" : "https://localhost:5554/mgmt/"
                }
            ]
        }
        with codecs.open(os.path.join(self.CONFIG_PATH, "config_restonic.json"), "w", "utf-8") as json_file:
            json.dump(config_example, json_file, sort_keys=True, indent=4, ensure_ascii=False)
