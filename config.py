import os
import codecs
import json

class Config:
    """ Represents the selected environment configuration
        There are 3 possible environments:
        1) dev
        2) test
        3) prod
        Each environmet has each own config file, so the default config wont be long.
    """

    CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "configurations")

    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        with codecs.open(os.path.join(self.CONFIG_PATH, "config_restonic.json"), "r", "utf-8") as json_file:
            return json.load(json_file) 
        