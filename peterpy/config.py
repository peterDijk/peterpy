from os import environ
from dotenv import load_dotenv

environment = environ.get("APP_ENV", "development")
load_dotenv(f".env.{environment}")  # take environment variables from .env.

# mypy: ignore-errors
from configloader import ConfigLoader

config = ConfigLoader()
config.update_from_yaml_file(f"config.{environment}.yaml")
config.update_from_env_namespace("PETERPY")
