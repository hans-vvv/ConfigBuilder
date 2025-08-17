import pandas as pd
from pathlib import Path

from app.utils import read_excel_to_df

BASE_DIR = Path(__file__).resolve().parents[2]  # root of the project
SRC_DIR = BASE_DIR / "src"


def get_dhcp_info_df() -> pd.DataFrame:
    """
    Returns DHCP info as DataFrame from ./src/dhcp_server_info.xlsx
    """

    # Resolve absolute path
    wb_path = SRC_DIR / "dhcp_server_info.xlsx"

    fields = {
        'Network Name': 'network_name',
        'Subnet Name': 'subnet_name',
        'Gateway IP': 'gwip',
        'Lease Time': 'lease_time',
        'Name server template': 'ns_templ',
        'DHCP options template': 'dhcp_templ',
    }

    return read_excel_to_df(wb_path, "DHCP info", fields)


def get_dhcp_options_templates_df() -> pd.DataFrame:
    """
    Returns DHCP options templates as DataFrame.
    """
    wb_path = SRC_DIR / "dhcp_server_info.xlsx"
    fields = {
        'DHCP options template': 'template',
        'Code1': 'c1', 'Type1': 't1', 'Value1': 'v1',
        'Code2': 'c2', 'Type2': 't2', 'Value2': 'v2',
        'Code3': 'c3', 'Type3': 't3', 'Value3': 'v3',
        'Code4': 'c4', 'Type4': 't4', 'Value4': 'v4',
    }
    return read_excel_to_df(wb_path, "DHCP options templates", fields)


def get_name_server_templates_df() -> pd.DataFrame:
    """
    Returns Name server templates as DataFrame.
    """
    wb_path = SRC_DIR / "dhcp_server_info.xlsx"
    fields = {
        'Name server template': 'template',
        'Name servers': 'name_servers',
    }
    return read_excel_to_df(wb_path, "Name server templates", fields)
