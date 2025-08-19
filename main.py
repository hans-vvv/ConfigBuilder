from app.meraki_api import get_meraki_api
from app.views import DhcpView
from app.config_printer import write_configs


def main():  

    meraki_api = get_meraki_api(use_cache=True)

    dhcp_view = DhcpView(meraki_api)
    dhcp_subtree = dhcp_view.build_dhcp_subtree()
    write_configs(dhcp_subtree, output_dir="output_configs")

    # # Path to sample config file
    # config_path = os.path.join("test_configs", "TEST-config.txt")
    
    # # Load config file content
    # with open(config_path, "r") as f:
    #     config_text = f.read()

    # # Parse the configuration
    # parsed_tree = parser.parse_fortigate_config(config_text)

    # # Print parsed dict tree (or process as needed)
    # import json
    # print(json.dumps(parsed_tree, indent=4))




if __name__ == "__main__":
    main()
