import configparser
from typing import Dict, Any


def read_config(config_path: str) -> Dict[str, Any]:
    config = configparser.ConfigParser()
    config.read(config_path)
    return {s: dict([(key, eval(value)) for key, value in config.items(s)]) for s in config.sections()}
