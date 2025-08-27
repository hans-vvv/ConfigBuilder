import json

from app.utils import merge_nested_dicts
from app.src.mock_data.meraki_mock_data import get_mocked_static_routes

from app.models.excel_models import DhcpInfoQueries
from app.models.api_models import MerakiQueries

TEMPLATE_NAME = "dhcp_subtree.j2"
TEMPLATE_DIR = "app/templates/fortigate"
OUT_DIR = "app/test_output_configs"
SITE = 'BRUSSELS'

# Loads test data from an Excel file.
dhcp_info_queries = DhcpInfoQueries('app/src/mock_data/dhcp_info_mock.xlsx')
dhcp_info_data = dhcp_info_queries.get_dhcp_info_data(site_name=SITE)

# Loads Meraki test data
mock_data = get_mocked_static_routes()
meraki_queries = MerakiQueries()
meraki_data = meraki_queries.get_static_routes(
    site_name=SITE, mock_data=mock_data
)

# print(json.dumps(meraki_data, indent=4))


def merged_data():
    return merge_nested_dicts(dhcp_info_data, meraki_data)

# print(json.dumps(merged_data(), indent=4))


def run() -> None:

    from app.printers.printer import Printer
    printer = Printer(
        config_tree=merged_data(),
        template_name=TEMPLATE_NAME,
        template_dir=TEMPLATE_DIR,
        output_dir=OUT_DIR,
    )
    printer.render_to_files()
