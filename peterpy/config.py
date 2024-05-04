from os import environ

from configloader import ConfigLoader

config = ConfigLoader()
environment = environ.get("APP_ENV", "development")
config.update_from_yaml_file(f"config.{environment}.yaml")
