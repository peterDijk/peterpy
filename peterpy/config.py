from os import environ

# mypy: ignore-errors
from configloader import ConfigLoader
from dotenv import load_dotenv

environment = environ.get("APP_ENV", "development")
load_dotenv(".env")  # take environment variables from .env.

config = ConfigLoader()
config.update_from_yaml_file(f"config.{environment}.yaml")
config.update_from_env_namespace("PETERPY")
