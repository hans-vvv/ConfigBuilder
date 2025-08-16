import os
import pickle
import ipaddress

from collections import defaultdict
from typing import Dict, Any

import pandas as pd

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from meraki_info import StaticRoute

from utils import Tree, read_excel_to_df


class ConfigGenerator:

    """
    This class can be used to print configurations for Fortigate appliances based on
    information present in an Excel file.
    """

    DEFAULT_WORKBOOK_NAME = 'meraki_additional_configuration.xlsx'
    CACHE_DIR = ".cache"

    def __init__(self, use_cache: bool = False):

        self.wb_name = None
        self.api_data = {}
        self.data_frames = {}
        self.config_tree = Tree()
        self.use_cache = use_cache
        os.makedirs(self.CACHE_DIR, exist_ok=True)

        if self.use_cache:
            self._load_cache()

    def _save_cache(self):
        """Serialize all data_frames into cache folder"""
        for name, df in self.data_frames.items():
            path = os.path.join(self.CACHE_DIR, f"{name}.pkl")
            with open(path, "wb") as f:
                pickle.dump(df, f)

    def _load_cache(self):
        """Load cached DataFrames into memory"""
        for file in os.listdir(self.CACHE_DIR):
            if file.endswith(".pkl"):
                name = file[:-4]
                with open(os.path.join(self.CACHE_DIR, file), "rb") as f:
                    self.data_frames[name] = pickle.load(f)

    def set_api_data(self, key: str, data: Any) -> None:
        """
        Store API data (like static_routes, vlans, etc.) for later normalization.
        """
        self.api_data[key] = data

    def initialize(self, workbook_name=None):
        self.wb_name = workbook_name or self.DEFAULT_WORKBOOK_NAME
        self._collect_data_frames()
        self._merge_data_in_config_tree()

    def _collect_data_frames(self, print_df_data: str = "") -> None:
        """
        Collects all DataFrames either from cache (if available)
        or from API/Excel, and updates cache if not using cache mode.

        print_df_data kwarg is key name of self.data_frames dict. Use for debugging.
        """
        if self.use_cache and self.data_frames:
            pass  # already loaded in __init__
        else:
            self.data_frames['dhcp_info'] = self._get_dhcp_info_data()
            self.data_frames['dhcp_options'] = self._get_dhcp_options_template_data()
            self.data_frames['name_server'] = self._get_name_server_data()
            self.data_frames['static_bindings'] = self._get_static_bindings_data()
            self.data_frames['reserved_ranges'] = self._get_reserved_ranges_data()

            # Always refresh cache when building from source
            self._save_cache()

        # Debugging: print DataFrame if requested
        if print_df_data:
            df = self.data_frames.get(print_df_data)
            if df is not None and not df.empty:
                print(df.to_string(index=False))
            else:
                print(f"[WARN] No DataFrame found for key '{print_df_data}' or it's empty.")

    def _merge_data_in_config_tree(self) -> None:

        self._merge_static_bindings_in_config_tree()
        self._merge_reserved_ranges_in_config_tree()
        self._merge_dhcp_info_in_config_tree()

    def _get_dhcp_options_template_data(self) -> pd.DataFrame:
        fields = {
            'DHCP options template': 'template',
            'Code1': 'c1', 'Type1': 't1', 'Value1': 'v1',
            'Code2': 'c2', 'Type2': 't2', 'Value2': 'v2',
            'Code3': 'c3', 'Type3': 't3', 'Value3': 'v3',
            'Code4': 'c4', 'Type4': 't4', 'Value4': 'v4',
        }
        return read_excel_to_df(self.wb_name, "DHCP options templates", fields)

    def _get_dhcp_info_data(self) -> pd.DataFrame:
        """
        Returns DHCP info as DataFrame
        """
        fields = {
            'Network Name': 'network_name',
            'Subnet Name': 'subnet_name',
            'Gateway IP': 'gwip',
            'Lease Time': 'lease_time',
            'Name server template': 'ns_templ',
            'DHCP options template': 'dhcp_templ',
        }
        return read_excel_to_df(self.wb_name, "DHCP info", fields)

    def _get_name_server_data(self) -> pd.DataFrame:
        """
        Returns Name server info as DataFrame
        """
        fields = {
            'Name server template': 'template',
            'Name servers': 'name_servers',
        }
        return read_excel_to_df(self.wb_name, "Name server templates", fields)

    def _get_static_bindings_data(self) -> pd.DataFrame:
        """
        Returns Static bindings as a DataFrame, normalized from API data.
        """
        routes: list[StaticRoute] = self.api_data.get("static_routes", [])
        if not routes:
            return pd.DataFrame(columns=["network_name", "subnet_name", "ip", "mac", "description"])

        rows = []
        for r in routes:
            if not r.fixed_ip_assignments:
                continue

            for mac, assignment in r.fixed_ip_assignments.items():
                rows.append({
                    "network_name": getattr(r, "network_name", None),
                    "subnet_name": getattr(r, "name", None),
                    "ip": assignment.get("ip"),
                    "mac": mac,
                    "description": assignment.get("name"),
                })

        return pd.DataFrame(rows)

    def _get_reserved_ranges_data(self) -> pd.DataFrame:
        """
        Normalize reserved IP ranges from API data into one row per range.
        """
        rows = []
        for route in self.api_data.get('static_routes', []):
            for r in getattr(route, "reserved_ip_ranges", []):  # list of dicts
                rows.append({
                    "network_name": route.network_name,
                    "subnet_name": route.name,
                    "start": r.get("start"),
                    "end": r.get("end"),
                })

        return pd.DataFrame(rows, columns=["network_name", "subnet_name", "start", "end"])

    def _merge_static_bindings_in_config_tree(self) -> None:
        """
        Attach static_bindings to each subnet subtree in config_tree.
        Bindings are normalized per subnet_name and inserted as a list of dicts.
        If a subnet has no bindings, an empty list is attached.
        """
        bindings = defaultdict(list)
        for row in self.data_frames['static_bindings'].itertuples(index=False):
            bindings[row.subnet_name].append(
                {'ip': row.ip, 'mac': row.mac, 'description': row.description}
            )

        for network_name, network in self.config_tree['networks'].items():
            for subnet_name, subtree in network['static_routes'].items():
                subtree['static_bindings'] = bindings[subnet_name]

    def _merge_reserved_ranges_in_config_tree(self) -> None:
        """
        Attach reserved_ranges to each subnet subtree in config_tree.
        Reserved ranges are normalized per subnet_name and stored as a list of dicts.
        """
        reserved_ranges = defaultdict(list)

        # Collect ranges from the reserved_ranges DataFrame
        for row in self.data_frames['reserved_ranges'].itertuples(index=False):
            if row.start is None:
                continue
            reserved_ranges[row.subnet_name].append({'start': row.start, 'end': row.end})

        # Attach collected reserved ranges to the config_tree
        for network_name, network in self.config_tree['networks'].items():
            for subnet_name, subtree in network['static_routes'].items():
                subtree['reserved_ranges'] = reserved_ranges[subnet_name]

    def _get_dhcp_options(self, template: str) -> list[dict]:
        """
        Extract DHCP options for a given template from the dhcp_options DataFrame.
        Returns a list of dicts with keys: code, type, value.
        """
        df = self.data_frames.get("dhcp_options")
        if df is None or df.empty:
            return []

        result = []
        template_rows = df[df["template"] == template]

        for _, row in template_rows.iterrows():
            # loop over the numbered option sets (1..4)
            for i in range(1, 5):
                code = row.get(f"c{i}")
                if pd.notna(code):
                    result.append({
                        "code": code,
                        "type": row.get(f"t{i}"),
                        "value": row.get(f"v{i}"),
                    })
        return result

    def _get_name_servers(self, template: str) -> list[str]:
        """
        Extract name servers for a given template from the name_server DataFrame.
        Returns a list of IPs/hostnames as strings.
        """
        df = self.data_frames.get("name_server")
        if df is None or df.empty:
            return []

        result = []
        template_rows = df[df["template"] == template]

        for _, row in template_rows.iterrows():
            if pd.notna(row.get("name_servers")):
                result.extend([ns.strip() for ns in row["name_servers"].split(",") if ns.strip()])

        return result

    def _merge_dhcp_info_in_config_tree(self) -> None:
        """
        Attach DHCP configuration info to each subnet subtree in config_tree.
        Pulls data from the dhcp_info DataFrame, resolves supporting info
        (name servers, DHCP options, subnet ranges/netmask), and inserts it.
        """

        # Build lookup from (network_name, subnet_name) → StaticRoute object
        route_by_key = {
            (r.network_name, r.name): r
            for r in self.api_data.get("static_routes", [])
        }

        for row in self.data_frames['dhcp_info'].itertuples(index=False):
            # Skip if no gateway IP defined for this subnet
            if row.gwip is None:
                continue

            # Expand references to templates
            name_servers = self._get_name_servers(row.ns_templ)
            dhcp_options = self._get_dhcp_options(row.dhcp_templ)

            # Lookup matching StaticRoute object
            static_route = route_by_key.get((row.network_name, row.subnet_name))
            if not static_route:
                continue  # skip if no corresponding static route found

            # Get calculated subnet details (start/end/netmask)
            subnet_details = self._get_subnet_details(static_route.subnet)
            start_ip = subnet_details['lowest_ip']
            end_ip = subnet_details['highest_ip']
            netmask = subnet_details['netmask']

            # Build the DHCP info payload
            dhcp_info = {
                'gwip': row.gwip,
                'lease': row.lease_time,
                'name_servers': name_servers,
                'dhcp_options': dhcp_options,
                'start_ip': start_ip,
                'end_ip': end_ip,
                'netmask': netmask,
            }

            # Attach it to the correct subnet subtree
            subtree = self.config_tree['networks'][row.network_name]['static_routes'][row.subnet_name]
            subtree['dhcp_info'] = dhcp_info

    @staticmethod
    def _get_subnet_details(subnet: str) -> dict[str, str | None]:
        """
        Given a subnet in CIDR notation, return details about the usable IP range.

        Args:
            subnet (str): Subnet string in CIDR format (e.g. "192.168.1.0/24").

        Returns:
            dict[str, str | None]: Dictionary with keys:
                - "lowest_ip": First usable host IP (or None if no usable hosts).
                - "highest_ip": Last usable host IP (or None if no usable hosts).
                - "netmask": Subnet mask as string.
        """
        network = ipaddress.ip_network(subnet, strict=False)
        hosts = list(network.hosts())  # excludes network and broadcast addresses

        return {
            "lowest_ip": str(hosts[0]) if hosts else None,
            "highest_ip": str(hosts[-1]) if hosts else None,
            "netmask": str(network.netmask),
        }

    @staticmethod
    def _jinja2_parser(j2template_name: str, **kwargs: Dict[str, Any]) -> str:
        """
        Render a Jinja2 template into a string.

        Args:
            j2template_name (str): Name of the template file (must be located in `j2templates/`).
            **kwargs (Dict[str, Any]): Key-value pairs passed to the template context.

        Returns:
            str: The rendered template as a string.
        """
        file_loader = FileSystemLoader("j2templates")
        env = Environment(
            loader=file_loader,
            trim_blocks=True,
            lstrip_blocks=True,
            undefined=StrictUndefined,  # raise error if template variable is missing
        )
        env.add_extension("jinja2.ext.loopcontrols")

        template = env.get_template(j2template_name)
        return template.render(**kwargs)

    def _render_config_for_subtree(self, subtree: Tree) -> str:
        """
        Render configuration text for a given subtree of the config tree.

        Args:
            subtree (Tree): A subtree of the configuration tree (typically corresponding
                            to one network or a subset of its settings).

        Returns:
            str: The rendered configuration as plain text.
        """
        return self._jinja2_parser("subtree.txt", subtree=subtree)

    def write_configs(self, output_dir: str = ".") -> None:
        """
        Generate and write configuration files for each network in the config tree.

        Args:
            output_dir (str, optional): Directory where the config files should be written.
                                        Defaults to the current directory ("./").

        Notes:
            - Currently hardcoded to only render configs for the "BRUSSELS" network.
              Other networks are skipped.
            - Output files are named `<network_name>-config.txt`.
        """
        for network_name, network_subtree in self.config_tree["networks"].items():
            if network_name != "BRUSSELS":  # TODO: remove filter to support all networks
                continue

            config_text = self._render_config_for_subtree(network_subtree)
            output_path = os.path.join(output_dir, f"{network_name}-config.txt")

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(config_text)
