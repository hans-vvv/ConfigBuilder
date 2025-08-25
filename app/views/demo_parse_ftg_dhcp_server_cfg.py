import json
from app.cli_parsers.parsers import parse_fortigate_config

CFG_FILE = 'app/test_output_configs/brussels.cfg'
DISSECTOR_FILE = 'app/templates/fortigate/fortigate_dissector.yaml'

config_tree = parse_fortigate_config(CFG_FILE, DISSECTOR_FILE)


def run():
    print(json.dumps(config_tree, indent=4))
