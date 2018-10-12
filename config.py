import os
import codecs
import json
import click

class Config:
    """ Represents the selected environment configuration
    """

    CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "configurations")
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
        
    def generate_config(self):
        config_example = {
            "comment" : "An example file",
            "datapower_rest_url" : "https://localhost:5554/mgmt/",
            "credentials" : {
                "username" : "admin",
                "password" : "admin"
            }
        }
        with codecs.open(os.path.join(self.CONFIG_PATH, "config_restonic.json"), "w", "utf-8") as json_file:
            json.dump(config_example, json_file, sort_keys=True, indent=4, ensure_ascii=False)