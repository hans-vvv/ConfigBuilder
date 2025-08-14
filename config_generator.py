from collections import defaultdict
from typing import Dict, Any
import ipaddress

from openpyxl import load_workbook
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from utils import read_excel_tab, Tree


class ConfigGenerator:

    """
    This class can be used to print configurations for Fortigate appliances based on
    information present in an Excel file.
    """

    WORKBOOK_NAME = 'result.xlsx'

    def __init__(self):

        self.wb = load_workbook(self.WORKBOOK_NAME)
        self.raw_excel_data = {}
        self.config_tree = Tree()

        self._read_all_tabs()
        self._merge_data_in_config_tree()

    def _read_all_tabs(self):

        self.raw_excel_data['dhcp_options'] = self._get_dhcp_options_template_data()
        self.raw_excel_data['static_bindings'] = self._get_static_bindings_data()
        self.raw_excel_data['reserved_ranges'] = self._get_reserved_ranges_data()
        self.raw_excel_data['static_routes'] = self._get_static_routes_data()
        self.raw_excel_data['dhcp_info'] = self._get_dhcp_info_data()
        self.raw_excel_data['name_server'] = self._get_name_server_data()

    def _merge_data_in_config_tree(self):

        self._initialize_static_routes_subtrees()
        self._merge_static_bindings_in_config_tree()
        self._merge_reserved_ranges_in_config_tree()
        self._merge_dhcp_info_in_config_tree()
        # print(self.config_tree)
        # print(self._get_dhcp_options('8'))
        # print(self._get_name_servers('1'))

    def _get_dhcp_options_template_data(self):
        """
        Returns DHCP options templates as list of data class objects
        """
        fields = [
            ('DHCP options template', 'template'),
            ('Code1', 'c1'), ('Type1', 't1'), ('Value1', 'v1'),
            ('Code2', 'c2'), ('Type2', 't2'), ('Value2', 'v2'),
            ('Code3', 'c3'), ('Type3', 't3'), ('Value3', 'v3'),
            ('Code4', 'c4'), ('Type4', 't4'), ('Value4', 'v4'),
        ]
        return read_excel_tab(self.wb, 'DHCP options templates', fields)

    def _get_static_bindings_data(self):
        """
        Returns Static bindings as list of data class objects
        """
        fields = [
            ('Network Name', 'network_name'), ('Subnet Name', 'subnet_name'), ('IP address', 'ip'),
            ('MAC address', 'mac'), ('Description', 'description'),
        ]
        return read_excel_tab(self.wb, 'Static bindings', fields)

    def _get_reserved_ranges_data(self):
        """
        Returns Reserved ranges as list of data class objects
        """
        fields = [
            ('Network Name', 'network_name'), ('Subnet Name', 'subnet_name'), ('Start1', 'start1'),
            ('End1', 'end1'), ('Start2', 'start2'), ('End2', 'end2')
        ]
        return read_excel_tab(self.wb, 'Reserved ranges', fields)

    def _get_static_routes_data(self):
        """
        Returns Static Routes as list of data class objects
        """
        fields = [
            ('Network Name', 'network_name'), ('Subnet Name', 'subnet_name'), ('Subnet', 'subnet'),
            ('Enabled', 'enabled'),
        ]
        return read_excel_tab(self.wb, 'Static routes', fields)

    def _get_dhcp_info_data(self):
        """
        Returns DHCP info as list of data class objects
        """
        fields = [
            ('Network Name', 'network_name'), ('Subnet Name', 'subnet_name'), ('Gateway IP', 'gwip'),
            ('Lease Time', 'lease_time'), ('Name server template', 'ns_templ'), ('DHCP options template', 'dhcp_templ')
        ]
        return read_excel_tab(self.wb, 'DHCP info', fields)

    def _get_name_server_data(self):
        """
        Returns Name server info as list of data class objects
        """
        fields = [
            ('Name server template', 'template'), ('Name servers', 'name_servers'),
        ]
        return read_excel_tab(self.wb, 'Name server templates', fields)

    def _initialize_static_routes_subtrees(self):

        for row in self.raw_excel_data['static_routes']:
            head = self.config_tree['networks'][row.network_name]['static_routes']
            result = {'name': row.subnet_name, 'subnet': row.subnet, 'enabled': row.enabled}
            head[row.subnet_name] = result

    def _merge_static_bindings_in_config_tree(self):

        bindings = defaultdict(list)
        for row in self.raw_excel_data['static_bindings']:
            bindings[row.subnet_name].append((row.ip, row.mac, row.description))

        for network_name in self.config_tree['networks']:
            for subnet_name in self.config_tree['networks'][network_name]['static_routes']:
                head = self.config_tree['networks'][network_name]['static_routes'][subnet_name]
                head.update({'static_bindings': bindings[subnet_name]})

    def _merge_reserved_ranges_in_config_tree(self):

        reserved_ranges = defaultdict(list)
        for row in self.raw_excel_data['reserved_ranges']:
            if row.start1 is None:
                continue
            reserved_ranges[row.subnet_name].append({'start': row.start1, 'end': row.end1})
            if row.start2 is not None:
                reserved_ranges[row.subnet_name].append({'start': row.start2, 'end': row.end2, })

        for network_name in self.config_tree['networks']:
            for subnet_name in self.config_tree['networks'][network_name]['static_routes']:
                head = self.config_tree['networks'][network_name]['static_routes'][subnet_name]
                head.update({'reserved_ranges': reserved_ranges[subnet_name]})

    def _get_dhcp_options(self, template):

        result = []
        for row in self.raw_excel_data['dhcp_options']:
            if template != row.template:
                continue
            result.append({'code': row.c1, 'type': row.t1, 'value': row.v1})
            if row.c2 is not None:
                result.append({'code': row.c2, 'type': row.t2, 'value': row.v2})
            if row.c3 is not None:
                result.append({'code': row.c3, 'type': row.t3, 'value': row.v3})
            if row.c4 is not None:
                result.append({'code': row.c4, 'type': row.t4, 'value': row.v4})
        return result

    def _get_name_servers(self, template):
        for row in self.raw_excel_data['name_server']:
            if template != row.template:
                continue
            return row.name_servers.split(',')

    def _merge_dhcp_info_in_config_tree(self):

        for row in self.raw_excel_data['dhcp_info']:
            if row.gwip is None:
                continue

            name_servers = self._get_name_servers(row.ns_templ)
            dhcp_options = self._get_dhcp_options(row.dhcp_templ)
            subnet_name_from_dhcp_info = row.subnet_name

            subnet = ''
            for static_route_row in self.raw_excel_data['static_routes']:
                if static_route_row.subnet_name == subnet_name_from_dhcp_info:
                    subnet = static_route_row.subnet

            start_ip = self._get_subnet_details(subnet)['lowest_ip']
            end_ip = self._get_subnet_details(subnet)['highest_ip']
            netmask = self._get_subnet_details(subnet)['netmask']

            dhcp_info = {
                'gwip': row.gwip,
                'lease': row.lease_time,
                'name_servers': name_servers,
                'dhcp_options': dhcp_options,
                'start_ip': start_ip,
                'end_ip': end_ip,
                'netmask': netmask,
            }
            head = self.config_tree['networks'][row.network_name]['static_routes'][row.subnet_name]
            head.update({'dhcp_info': dhcp_info})

    @staticmethod
    def _get_subnet_details(subnet_str):
        try:
            network = ipaddress.ip_network(subnet_str, strict=False)
            hosts = list(network.hosts())

            return {
                "lowest_ip": str(hosts[0]) if hosts else None,
                "highest_ip": str(hosts[-1]) if hosts else None,
                "netmask": str(network.netmask)
            }
        except ValueError as e:
            return {"error": str(e)}

    @ staticmethod
    def _j2_parser(j2template_name: str, **kwargs: Dict[str, Any]) -> str:
        """
        Jinja2 parser
         """
        file_loader = FileSystemLoader('j2templates')
        env = Environment(
            loader=file_loader, trim_blocks=True, lstrip_blocks=True,
            undefined=StrictUndefined
        )
        env.add_extension('jinja2.ext.loopcontrols')
        j2template = env.get_template(j2template_name)

        return j2template.render(**kwargs)

    def _parse_subtree(self, subtree):
        """
        Wrapper to print configuration based on provide subtree
        """
        kwargs = {'subtree': subtree}
        return self._j2_parser('subtree.txt', **kwargs)

    def print_configs(self) -> None:
        """
        Print one config per device
        """

        for network_name in self.config_tree['networks']:
            if network_name != 'BRUSSELS':
                continue
            print(self.config_tree['networks'][network_name])
            with open(network_name + '-config.txt', 'w') as f:
                config = self._parse_subtree(self.config_tree['networks'][network_name])
                print(config, file=f)
