import yaml
import json
from typing import Any


def read_yaml(path: str):
    with open(path, 'r') as yaml_file:
        data = yaml.load(yaml_file, Loader=yaml.FullLoader)
    return data


def read_json(path: str):
    with open(path, 'r') as json_file:
        data = json.load(json_file)
    return data


def write_yaml_file(data: Any, file_path: str):
    with open(file_path, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


def write_json_file(data: Any, file_path: str):
    with open(file_path, 'w') as outfile:
        json.dump(data, outfile, indent=4)
