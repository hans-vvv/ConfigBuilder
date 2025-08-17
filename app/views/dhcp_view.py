import json
from collections import defaultdict

import ipaddress
import pandas as pd

from app.template_data import (
    get_dhcp_info_df,
    get_dhcp_options_templates_df,
    get_name_server_templates_df,
)
from app.meraki_api import meraki_api


def build_dhcp_subtree() -> dict:
    """Build DHCP server config subtree."""

    # 1) Load sources
    df_dhcp = get_dhcp_info_df()
    df_options = get_dhcp_options_templates_df()
    df_nameservers = get_name_server_templates_df()
    df_static_routes = meraki_api.get_static_routes()  # <- returns a DataFrame

    # 2) Join DHCP info with static routes (to get subnet, fixed/reserved, etc.)
    merged = df_dhcp.merge(
        df_static_routes,
        left_on="subnet_name",   # Excel
        right_on="name",         # Meraki route name
        how="left",
    )

    # 3) Join template tables
    merged = merged.merge(
        df_options,
        left_on="dhcp_templ",
        right_on="template",
        how="left",
        suffixes=("", "_opt"),
    )
    merged = merged.merge(
        df_nameservers,
        left_on="ns_templ",
        right_on="template",
        how="left",
        suffixes=("", "_ns"),
    )

    # print(merged.to_string(index=False))
    # print(merged.columns)

    def _subnet_details(subnet: str) -> dict:
        try:
            if not subnet or pd.isna(subnet):
                return {k: None for k in ("netmask", "start_ip", "end_ip", "lowest_ip", "highest_ip")}
            net = ipaddress.ip_network(subnet, strict=False)
            hosts = list(net.hosts())
            low = str(hosts[0]) if hosts else None
            high = str(hosts[-1]) if hosts else None
            return {
                "netmask": str(net.netmask),
                "start_ip": low,
                "end_ip": high,
                "lowest_ip": low,
                "highest_ip": high,
            }
        except ValueError:
            return {k: None for k in ("netmask", "start_ip", "end_ip", "lowest_ip", "highest_ip")}

    def _expand_dhcp_options(row) -> list[dict]:
        opts = []
        for i in range(1, 5):
            code = getattr(row, f"c{i}", None)
            if code is None or (isinstance(code, float) and pd.isna(code)) or str(code).strip() == "":
                continue
            opts.append({
                "code": code,
                "type": getattr(row, f"t{i}", None),
                "value": getattr(row, f"v{i}", None),
            })
        return opts

    def _parse_name_servers(raw) -> list[str]:
        if raw is None or (isinstance(raw, float) and pd.isna(raw)):
            return []
        return [p.strip() for p in str(raw).split(",") if p.strip()]

    def _extract_bindings(row) -> list[dict]:
        bindings = []
        fia = getattr(row, "fixed_ip_assignments", None)
        if isinstance(fia, dict):
            for mac, info in fia.items():
                bindings.append({"ip": info.get("ip"), "mac": mac, "description": info.get("name")})
        return bindings

    def _extract_reserved_ranges(row) -> list[dict]:
        ranges = []
        rir = getattr(row, "reserved_ip_ranges", None)
        if isinstance(rir, list):
            for r in rir:
                start, end = r.get("start"), r.get("end")
                if start and end:
                    ranges.append({"start": start, "end": end})
        return ranges

    # 4) Build config-tree dict
    dhcp_tree = defaultdict(dict)
    for row in merged.itertuples(index=False):
        details = _subnet_details(getattr(row, "subnet", None))

        dhcp_tree[row.network_name_x][row.subnet_name] = {
            "gwip": row.gwip,
            "lease": row.lease_time,
            "subnet": getattr(row, "subnet", None),
            "netmask": details["netmask"],
            "start_ip": details["start_ip"],
            "end_ip": details["end_ip"],
            "name_servers": _parse_name_servers(getattr(row, "name_servers", None)),
            "dhcp_options": _expand_dhcp_options(row),
            "static_bindings": _extract_bindings(row),
            "reserved_ranges": _extract_reserved_ranges(row),
            # optional extras if you want them downstream
            "network_name": row.network_name_x,
            # "network_name": getattr(row, "network_name", None),
            "route_name": getattr(row, "name", None),
        }
    # print(json.dumps(dhcp_tree, indent=4))
    return dhcp_tree
