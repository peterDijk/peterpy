from os import environ

from configloader import ConfigLoader

config = ConfigLoader()
config.update_from_yaml_file("config.yaml")
environment = environ.get("APP_ENV", "development")
