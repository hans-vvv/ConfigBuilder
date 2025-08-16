import json
from typing import Optional
from dataclasses import dataclass, field

import meraki

import pandas as pd
from pathlib import Path


@dataclass
class StaticRoute:
    network_id: str
    network_name: str
    name: str
    subnet: str
    gateway_ip: str
    enabled: bool
    fixed_ip_assignments: Optional[dict] = field(default_factory=dict)
    reserved_ip_ranges: Optional[list] = field(default_factory=list)
    comment: Optional[str] = None


class MerakiApiManager:

    def __init__(self):
        self.dashboard = None
        self._all_structured_routes = None  # cache for static routes

    def initialize(self, api_key, print_console=False, suppress_logging=True):
        self.dashboard = meraki.DashboardAPI(
            api_key=api_key, print_console=print_console, suppress_logging=suppress_logging,
        )

    def get_structured_static_routes(self) -> list[StaticRoute]:
        if not self.dashboard:
            raise RuntimeError("Meraki dashboard client not initialized. Call initialize() first.")

        if self._all_structured_routes is not None:
            return self._all_structured_routes

        all_structured_routes = []

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
                            all_structured_routes.append(
                                StaticRoute(
                                    network_id=network_id,
                                    network_name=network_name,
                                    name=route.get('name', ''),
                                    subnet=route.get('subnet', ''),
                                    gateway_ip=route.get('gatewayIp', ''),
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

        self._all_structured_routes = all_structured_routes  # cache
        return all_structured_routes


class MerakiExcelExporter:
    def __init__(self, routes: list[StaticRoute]):
        self.routes = routes

    def export_to_excel(self, filepath: str | Path):
        filepath = Path(filepath)
        print(f"Exporting to {filepath.resolve()}...")

        # Sheet 1: All Routes (with properly expanded values)
        df_all_routes = pd.DataFrame([
            {
                'Network Name': r.network_name,
                'Route Name': r.name,
                'Subnet': r.subnet,
                'Enabled': r.enabled,
            }
            for r in self.routes
        ])

        # Sheet 2: Fixed IPs
        reservation_rows = []
        for r in self.routes:
            for mac, info in r.fixed_ip_assignments.items():
                reservation_rows.append({
                    'Network Name': r.network_name,
                    'Route Name': r.name,
                    'MAC': mac,
                    'IP': info.get('ip', ''),
                    'Description': info.get('name', ''),
                })
        df_reservations = pd.DataFrame(reservation_rows)

        # Sheet 3: Reserved Ranges (as literal column)
        reserved_rows = []
        for r in self.routes:
            if r.reserved_ip_ranges:  # Only include if ranges exist
                reserved_rows.append({
                    'Network Name': r.network_name,
                    'Route Name': r.name,
                    'Reserved Ranges': json.dumps(r.reserved_ip_ranges, indent=2)
                })
        df_reserved = pd.DataFrame(reserved_rows)

        # Write to Excel (with headers and formatting)
        with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
            df_all_routes.to_excel(writer, sheet_name='All Routes', index=False)
            df_reservations.to_excel(writer, sheet_name='Fixed IPs', index=False)
            df_reserved.to_excel(writer, sheet_name='Reserved Ranges', index=False)

        print("✅ Export completed.")
