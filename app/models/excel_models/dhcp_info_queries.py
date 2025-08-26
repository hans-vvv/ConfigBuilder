import pandas as pd

from .base_excel_data_loader import BaseExcelDataLoader


class DhcpInfoQueries(BaseExcelDataLoader):
  
    def _get_name_servers_for_subnet(self, network_name: str, subnet_name: str) -> list[str]:
        """
        Get the list of name server addresses for the given network and subnet.
        
        Args:
            network_name (str): The name of the network.
            subnet_name (str): The name of the subnet.

        Returns:
            list[str]: List of name server IP addresses.

        Raises:
            ValueError: If required sheets or columns are missing.
            LookupError: If no name servers are found for the specified subnet.
        """
        try:
            dhcp_info_df = self.get_dataframe_from_sheet('DhcpInfo')
            name_server_templates_df = self.get_dataframe_from_sheet('NameServerTemplate')
            name_servers_df = self.get_dataframe_from_sheet('NameServer') 
        except ValueError as e:
            raise ValueError(f"Missing sheet or required column: {e}")

        filtered_dhcp = dhcp_info_df[
            (dhcp_info_df['network_name'] == network_name) &
            (dhcp_info_df['subnet_name'] == subnet_name)
        ]
        if filtered_dhcp.empty:
            raise LookupError(f"No DHCP info found for network '{network_name}', subnet '{subnet_name}'.")
        ns_template_name = filtered_dhcp.iloc[0]['ns_template']
        filtered_template = name_server_templates_df[
            name_server_templates_df['template_name'] == ns_template_name
        ]        
        if filtered_template.empty:
            raise LookupError(f"No name server template found with name '{ns_template_name}'.")
        joined = pd.merge(
            filtered_template,
            name_servers_df,
            left_on='name_servers',
            right_on='id',
            how='inner'
        )
        addresses = joined['address'].drop_duplicates().tolist()        

        if not addresses:
            raise LookupError(f"No name server addresses found for template '{ns_template_name}'.")

        return addresses
    
    def _get_dhcp_options_for_subnet(self, network_name: str, subnet_name: str) -> list[dict]:
        """
        Get DHCP options for the given network and subnet.

        Args:
            network_name (str): The name of the network.
            subnet_name (str): The name of the subnet.

        Returns:
            list[dict]: List of DHCP option dictionaries with 'code', 'type', and 'value' keys.

        Raises:
            ValueError: If required sheets or columns are missing.
            LookupError: If no DHCP options are found for the specified subnet.
        """
        try:
            dhcp_info_df = self.get_dataframe_from_sheet('DhcpInfo')
            dhcp_options_templates_df = self.get_dataframe_from_sheet('DhcpOptionTemplate')
            dhcp_options_df = self.get_dataframe_from_sheet('DhcpOption')
        except ValueError as e:
            raise ValueError(f"Missing sheet or required column: {e}")

        filtered_dhcp = dhcp_info_df[
            (dhcp_info_df['network_name'] == network_name) &
            (dhcp_info_df['subnet_name'] == subnet_name)
        ]

        if filtered_dhcp.empty:
            raise LookupError(f"No DHCP info found for network '{network_name}', subnet '{subnet_name}'.")
        dhcp_options_template_name = filtered_dhcp.iloc[0]['dhcp_option_template']

        filtered_template = dhcp_options_templates_df[
            dhcp_options_templates_df['template_name'] == dhcp_options_template_name
        ]        

        if filtered_template.empty:
            raise LookupError(f"No DHCP options template found with name '{dhcp_options_template_name}'.")
        exploded_template = filtered_template.explode('dhcp_options')

        joined = pd.merge(
            exploded_template,
            dhcp_options_df,
            left_on='dhcp_options',
            right_on='id',
            how='inner'
        )
        options_df = joined[['code', 'type', 'value']].drop_duplicates()        
        results = options_df.to_dict(orient='records')
        
        if not results:
            raise LookupError(f"No DHCP options found for template '{dhcp_options_template_name}'.")

        return results
    
    def get_dhcp_info_data(self, site_name: str ):

        result = {}
        
        dhcp_info_df = self.get_dataframe_from_sheet('DhcpInfo')
        required_columns = ['network_name', 'subnet_name', 'gw_ip', 'lease_time', 'ns_template', 'dhcp_option_template']

        # Filter rows where all these columns are non-null and non-empty
        filtered_df = dhcp_info_df.dropna(subset=required_columns)

        # Optionally, filter out empty strings for string columns
        filtered_df = filtered_df[(filtered_df[required_columns].astype(str) != '').all(axis=1)]

        for row in filtered_df.itertuples(index=False):

            network_name = getattr(row, 'network_name', '')
            subnet_name = getattr(row, 'subnet_name', '')

            if network_name != site_name:
                continue

            if network_name not in result:
                result[network_name] = {}
            
            result[network_name][subnet_name] = {
                "gw_ip": getattr(row, "gw_ip", None),
                "lease_time": getattr(row, "lease_time", None),
                "name_servers": self._get_name_servers_for_subnet(network_name, subnet_name),
                "dhcp_options": self._get_dhcp_options_for_subnet(network_name, subnet_name),
            }
        return result
