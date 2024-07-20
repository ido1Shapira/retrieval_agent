import configparser
import os
from typing import Dict, Any

from dotenv import load_dotenv


def read_config(config_path: str) -> Dict[str, Any]:
    config = configparser.ConfigParser()
    config.read(config_path)
    return {s: dict([(key, eval(value)) for key, value in config.items(s)]) for s in config.sections()}


def get_variable_env(name: str) -> str:
    value = os.environ.get(name, None)
    if not value:
        load_dotenv()
        value = os.environ.get(name, None)
    return value
