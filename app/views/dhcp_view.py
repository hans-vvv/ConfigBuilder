from app.core import merge_nested_dicts

from app.models import DhcpInfoQueries
from app.models import MerakiQueries

dhcp_info_queries = DhcpInfoQueries('src/dhcp_info_test.xlsx')
dhcp_info_queries.load()

meraki_queries = MerakiQueries()
meraki_queries.get_mock_meraki_data()

def merged_data():

    dhcp_info_data = dhcp_info_queries.get_dhcp_info_data()
    meraki_data = meraki_queries.get_mock_meraki_data()

    return merge_nested_dicts(dhcp_info_data, meraki_data)

def run() -> None:

    template_name = 'dhcp_subtree.j2'
    template_dir = 'app/templates/fortigate'
    out_path = 'output_configs'
    
    from app.printers import write_configs
    write_configs(
        config_tree=merged_data(), 
        template_name=template_name,
        template_dir=template_dir, 
        output_dir=out_path
    )





