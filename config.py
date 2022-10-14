import json
import os

default_config_path = "./config.json"
if os.path.isfile(default_config_path):
    with open(default_config_path, 'r') as f:
        config = json.load(f)