from app.services.meraki import get_meraki_api
from app.views import dhcp_view
from app.printers import write_configs


def main():  

    dhcp_view.run()

    # Path to sample config file
    # import os
    # from app.cli_parsers import parsers
    # config_path = os.path.join("test_configs", "TEST-config.txt")
    
    # # Load config file content
    # with open(config_path, "r") as f:
    #     config_text = f.read()

    # # Parse the configuration
    # parsed_tree = parsers.parse_fortigate_config(config_text)

    # # Print parsed dict tree (or process as needed)
    # import json
    # print(json.dumps(parsed_tree, indent=4))


if __name__ == "__main__":
    main()
