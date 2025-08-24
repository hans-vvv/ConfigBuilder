import ipaddress
import pandas as pd
from typing import Any
from app.api import get_meraki_api
from app.models.api_models import StaticRoute

class MerakiQueries:

    def __init__(self, auto_load: bool = True) -> None:
        """Initialize instance, setting up the Meraki API client and cache."""
        self.meraki_api = get_meraki_api
        self.dashboard = None  
        self.use_cache: bool | None = None
        self.cached_data: dict[str, Any] = {}
        if auto_load:
            self._load_env()        
  
    def _load_env(self) -> None:
        """Initialize the Meraki dashboard API client."""
        self.dashboard = self.meraki_api.get_dashbord() 
    
    @staticmethod
    def _subnet_details(subnet: str) -> dict:
        """Helper to extract info from a given subnet in CIDR notation."""
        try:
            if not subnet:
                return {k: None for k in ("netmask", "start_ip", "end_ip")}
            net = ipaddress.ip_network(subnet, strict=False)
            hosts = list(net.hosts())
            low = str(hosts[0]) if hosts else None
            high = str(hosts[-1]) if hosts else None
            return {
                "netmask": str(net.netmask),
                "start_ip": high,
                "end_ip": low                
            }
        except ValueError:
            return {k: None for k in ("netmask", "start_ip", "end_ip")}
    
    @staticmethod
    def _static_bindings(df_row: pd.Series) -> list[dict]:
        """Helper to extract info from a given DataFrame row."""
        bindings = []
        fia = getattr(df_row, "fixed_ip_assignments", None)
        if isinstance(fia, dict):
            for mac, info in fia.items():
                bindings.append({"ip": info.get("ip"), "mac": mac, "description": info.get("name")})
        return bindings

    @staticmethod
    def _extract_reserved_ranges(df_row: pd.Series) -> list[dict]:
        """Helper to extract info from a given DataFrame row."""
        ranges = []
        rir = getattr(df_row, "reserved_ip_ranges", None)
        if isinstance(rir, list):
            for r in rir:
                start, end = r.get("start"), r.get("end")
                if start and end:
                    ranges.append({"start": start, "end": end})
        return ranges

    def _load_static_routes_df(self, use_cache: bool) -> pd.DataFrame:        
        """Fetch static routes from Meraki API or cache as a pandas DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing static routes data.

        Raises:
            RuntimeError: If the dashboard client is not initialized or cache data is missing when expected.
        """
        if not self.dashboard:
            raise RuntimeError("Meraki dashboard client not initialized. Call _load_env first.")

        if self.use_cache and self.cached_data.get("static_routes") is not None:
            return self.cached_data["static_routes"]

        if self.use_cache:
            self.cached_data["static_routes"] = self.meraki_api.cache_controls.load("static_routes")
            if self.cached_data["static_routes"] is not None:                
                return self.cached_data["static_routes"]
            else:
                raise RuntimeError("No cached data available, first run from source and don't use cache")

        static_routes = []

        try:
            orgs = self.dashboard.organizations.getOrganizations()
            for org in orgs:
                networks = self.dashboard.organizations.getOrganizationNetworks(org['id'])
                for network in networks:
                    network_id = network['id']
                    network_name = network.get('name', '')

                    try:
                        routes = self.dashboard.appliance.getNetworkApplianceStaticRoutes(network_id)
                        for route in routes:
                            static_routes.append(
                                StaticRoute(                                    
                                    network_name=network_name,
                                    subnet_name=route.get('name', ''),
                                    subnet=route.get('subnet', ''),                                    
                                    enabled=route.get('enabled', True),
                                    fixed_ip_assignments=route.get('fixedIpAssignments', {}),
                                    reserved_ip_ranges=route.get('reservedIpRanges', []),
                                    comment=route.get('comment', None)
                                )
                            )
                    except Exception as e:
                        print(f"Error retrieving routes for {network_name} ({network_id}): {e}")

        except Exception as e:
            print(f"Error fetching organizations or networks: {e}")

        static_routes = pd.DataFrame([r for r in static_routes])
        if not self.use_cache:
            self.meraki_api.cache_controls.save("static_routes", static_routes)
        return static_routes
    
    def get_static_routes(self, use_cache: bool = True) -> dict[str, dict[str, Any | None]]: # type: ignore
        """Get static routes, optionally using cached data.

        Args:
            use_cache (bool): Whether to use cached data if available. Defaults to True.

        Returns:
            Dict containing transformed data.
        """
        result = {} 
        static_routes = self._load_static_routes_df(use_cache=use_cache)
        for row in static_routes.itertuples(index=False):
            
            network_name = getattr(row, "network_name", None)
            subnet_name = getattr(row, "subnet_name", None)

            if network_name not in result:
                result[network_name] = {}
            
            result[network_name][subnet_name] = {
                "enabled": getattr(row, "enabled", True),
                "subnet_details": self._subnet_details(getattr(row, "subnet", None)),  # type: ignore
                "static_bindings": self._static_bindings(getattr(row, "fixed_ip_assignmentst", None)), # type: ignore
                "reserved_ranges": self._extract_reserved_ranges(getattr(row, "reserved_ip_ranges", None)) # type: ignore
            }
        return result
    
    @staticmethod
    def get_mock_meraki_data() -> dict[str, dict[str, Any]]: # type: ignore
        """
        Returns mocked Meraki API data as a nested dictionary:
            - first key: network_name
            - second key: subnet_name
            - value: dict containing static route info (enabled, fixed_ip_assignments, reserved_ip_ranges, comment)

        This mimics the structure of StaticRoute instances grouped by network and subnet.
        """
        mock_data: dict[str, dict[str, Any]] = {
            "BRUSSELS": {
                "sub-1": {
                    "enabled": True,
                    "subnet": "1.1.1.0/24",
                    "fixed_ip_assignments": [
                        {"ip": "1.1.1.11", "mac": "04:42:1a:c9:99:9b", "description": "test1"},
                        {"ip": "1.1.1.12", "mac": "04:42:1a:c9:c9:9b", "description": "test2"},
                    ],
                    "reserved_ip_ranges": [
                        {"start": "1.1.1.1", "end": "1.1.1.10"}
                    ],
                    "start_ip": "1.1.1.1",
                    "end_ip": "1.1.1.254",
                    "comment": ""
                },
                "sub-2": {
                    "enabled": True,
                    "subnet": "2.2.2.0/24",
                    "fixed_ip_assignments": [
                        {"ip": "2.2.2.11", "mac": "05:42:1a:c9:99:9b", "description": "test3"},
                        {"ip": "2.2.2.12", "mac": "05:42:1a:c9:c9:9b", "description": "test4"},
                    ],
                    "reserved_ip_ranges": [
                        {"start": "2.2.2.1", "end": "2.2.2.10"}
                    ],
                    "start_ip": "2.2.2.1",
                    "end_ip": "2.2.2.254",
                    "comment": ""
                }
            }
        }
        return mock_data
