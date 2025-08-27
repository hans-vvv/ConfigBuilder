import ipaddress
from typing import Any

import pandas as pd

from app.api import get_meraki_api
from app.models.api_models.meraki_models import StaticRoute


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
        self.dashboard = self.meraki_api.get_dashboard()

    @staticmethod
    def _subnet_details(subnet: str) -> dict[str, str | None]:
        """Helper to extract info from a given subnet in CIDR notation."""
        net = ipaddress.ip_network(subnet, strict=False)
        hosts = list(net.hosts())
        low = str(hosts[0]) if hosts else None
        high = str(hosts[-1]) if hosts else None
        return {
            "netmask": str(net.netmask),
            "start_ip": low,
            "end_ip": high
        }

    @staticmethod
    def _static_bindings(raw_bindings: dict) -> list[dict]:
        """Helper to extract info from a given dict."""
        bindings = []
        if isinstance(raw_bindings, dict):
            for mac, info in raw_bindings.items():
                bindings.append({"ip": info.get("ip"), "mac": mac, "description": info.get("name")})
        return bindings

    @staticmethod
    def _extract_reserved_ranges(reserved_ranges: list[dict]) -> list[dict]:
        """Helper to extract info from a given dict."""
        ranges = []
        for reserved_range in reserved_ranges:
            start, end = reserved_range.get("start"), reserved_range.get("end")
            if start and end:
                ranges.append({"start": start, "end": end})
        return ranges

    def _load_static_routes_df(self, use_cache: bool, mock_data: list[StaticRoute] | None = None) -> pd.DataFrame:
        """Fetch static routes from Meraki API or cache as a pandas DataFrame.
           

        Returns:
            If mock_data is present then DataFrame containing mock data is returned
            pd.DataFrame: DataFrame containing static routes data.

        Raises:
            RuntimeError: If the dashboard client is not initialized or cache data is missing when expected.
        """

        if mock_data is not None:
            return pd.DataFrame([route for route in mock_data])

        if not self.dashboard:
            raise RuntimeError("Meraki dashboard client not initialized. Call _load_env first.")

        if use_cache and self.cached_data.get("static_routes") is not None:
            return self.cached_data["static_routes"]

        if use_cache:
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
                        # from app.models.api_models import StaticRoute
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
        if not use_cache:
            self.meraki_api.cache_controls.save("static_routes", static_routes)
        return static_routes

    def get_static_routes(self, site_name: str, use_cache: bool = True, mock_data: list[StaticRoute] | None = None
                          ) -> dict[str, dict[str, str]]:
        """Get static routes per site, optionally using cached data or mock_data

        Args:
            site_name: required argument.
            use_cache (bool): Whether to use cached data if available. Defaults to True.
            mock_data (list[StaticRoute])

        Returns:
            Dict containing transformed data.
        """
        result = {}
        static_routes = self._load_static_routes_df(use_cache=use_cache, mock_data=mock_data)
        for row in static_routes.itertuples(index=False):

            network_name = getattr(row, "network_name", None)
            subnet_name = getattr(row, "subnet_name", None)

            if site_name != network_name:
                continue

            if network_name not in result:
                result[network_name] = {}

            # print(getattr(row, "fixed_ip_assignments", None))
            # print(self._static_bindings(getattr(row, "fixed_ip_assignments", {}))) 
            # print((getattr(row, "reserved_ip_ranges", None)))
            # print(self._subnet_details(getattr(row, "subnet", str)))

            result[network_name][subnet_name] = {
                "enabled": getattr(row, "enabled", True),
                "subnet_details": self._subnet_details(getattr(row, "subnet", "")),
                "static_bindings": self._static_bindings(getattr(row, "fixed_ip_assignments", {})),
                "reserved_ip_ranges": self._extract_reserved_ranges(getattr(row, "reserved_ip_ranges", []))
            }

        return result
