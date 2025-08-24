# from app.views import test_create_ftg_dhcp_server_cfg
from app.views import demo_parse_ftg_dhcp_server_cfg
# from app.models import meraki_models
# from app.models import StaticRoute
# from app.core.utils import generate_excel_template
# from app.models.dhcp_info_model import (
#     DhcpInfo,    
#     DhcpOptionTemplate,
#     DhcpOption,
#     NameServerTemplate,
#     NameServer
# )


def main():  

    # test_create_ftg_dhcp_server_cfg.run()
    demo_parse_ftg_dhcp_server_cfg.run()
    
    

    # dataclasses = [
    #     DhcpInfo,    
    #     DhcpOptionTemplate,
    #     DhcpOption,
    #     NameServerTemplate,
    #     NameServer
    # ]
    # generate_excel_template('app/templates/excel_csv_templates/dhcp_info.xlsx', dataclasses)

    # dataclasses = [StaticRoute]
    # generate_excel_template('app/templates/excel_csv_templates/static_route.xlsx', dataclasses)

    # from app.models import DhcpInfoQueries

    # dhcp_info_queries = DhcpInfoQueries('src/dhcp_info_test.xlsx')
    # dhcp_info_queries.load()

    # dhcp_info_queries.pprint_df('DhcpInfo')
    # dhcp_info_queries.get_name_servers_for_subnet("BRUSSELS", "sub-1")
    # dhcp_info_queries.pprint_df(class_name='DhcpOption')
    # dhcp_info_queries.get_dhcp_options_for_subnet("BRUSSELS", "sub-1")
    # dhcp_info_queries.pprint_df(class_name='DhcpInfo')
    # dhcp_info_queries.pprint_df(class_name='DhcpOptionTemplate')
    # dhcp_info_queries.pprint_df(class_name='DhcpOption')
    # dhcp_info_queries.pprint_df(class_name='NameServerTemplate')
    # dhcp_info_queries.pprint_df(class_name='NameServer')

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
