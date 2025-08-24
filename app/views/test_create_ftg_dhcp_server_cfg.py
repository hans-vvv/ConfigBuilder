from app.utils import merge_nested_dicts

from app.models.excel_models import DhcpInfoQueries
from app.models.api_models import MerakiQueries

TEMPLATE_NAME = "dhcp_subtree.j2"
TEMPLATE_DIR  = "app/templates/fortigate"
OUT_DIR       = "app/test_output_configs"

# Loads test data from an Excel file.
dhcp_info_queries = DhcpInfoQueries('app/src/test/dhcp_info_test.xlsx')
dhcp_info_data = dhcp_info_queries.get_dhcp_info_data()

# Loads Meraki test data
meraki_queries = MerakiQueries()
meraki_data = meraki_queries.get_mock_meraki_data()

def merged_data():
    return merge_nested_dicts(dhcp_info_data, meraki_data)

def run() -> None:

    from app.printers.printer import Printer
    printer = Printer(
        config_tree=merged_data(),
        template_name=TEMPLATE_NAME,
        template_dir=TEMPLATE_DIR,
        output_dir=OUT_DIR,
    )
    printer.render_to_files()  





