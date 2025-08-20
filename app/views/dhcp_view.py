import ipaddress
import pandas as pd
from app.core.utils import coalesce

from app.services import (
    get_dhcp_info_df,    
    get_name_server_templates_df,
    get_dhcp_options_templates_df,
)

from app.services.meraki import get_meraki_api


def merge_transform(
    dhcp_info_df: pd.DataFrame,
    dhcp_options_templates_df: pd.DataFrame,
    name_server_templates_df: pd.DataFrame,
    static_routes_df: pd.DataFrame,
) -> dict:
    
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
    
    merged = dhcp_info_df.merge(
            static_routes_df,
            left_on="subnet_name",   # Excel
            right_on="name",         # Meraki route name
            how="left",
        )       
    merged = merged.merge(
            dhcp_options_templates_df,
            left_on="dhcp_templ",
            right_on="template",
            how="left",
            suffixes=("", "_opt"),
        )
    merged = merged.merge(
            name_server_templates_df,
            left_on="ns_templ",
            right_on="template",
            how="left",
            suffixes=("", "_ns"),
        )    
    # print(merged.to_string(index=False))
    # print(merged.columns)

    # Transform
    dhcp_tree = {}
    for row in merged.itertuples(index=False):
        
        details = _subnet_details(getattr(row, "subnet", None))  # type: ignore
        
        network_name = coalesce(getattr(row, "network_name_x", None), getattr(row, "network_name_y", None))
        subnet_name = coalesce(getattr(row, "subnet_name", None), getattr(row, "name", None))

        if network_name not in dhcp_tree:
            dhcp_tree[network_name] = {}

        dhcp_tree[network_name][subnet_name] = {
            "gwip": row.gwip,
            "lease": row.lease_time,
            "subnet": coalesce(getattr(row, "subnet", None)),  # normalized too!
            "netmask": details["netmask"],
            "start_ip": details["start_ip"],
            "end_ip": details["end_ip"],
            "name_servers": _parse_name_servers(getattr(row, "name_servers", None)),
            "dhcp_options": _expand_dhcp_options(row),
            "static_bindings": _extract_bindings(row),
            "reserved_ranges": _extract_reserved_ranges(row),
            "network_name": network_name,
            "route_name": getattr(row, "name", None),
        }
    return dhcp_tree


def run() -> None:

    template_name = 'dhcp_subtree.j2'
    template_dir = 'app/templates/fortigate'
    out_path = 'output_configs'

    meraki_api = get_meraki_api()

    static_routes_df = meraki_api.get_static_routes_df()
    dhcp_info_df = get_dhcp_info_df()
    dhcp_options_templates_df = get_dhcp_options_templates_df()
    name_server_templates_df = get_name_server_templates_df()
    
    dhcp_tree = merge_transform(
        dhcp_info_df,
        dhcp_options_templates_df,
        name_server_templates_df,
        static_routes_df,
    )
    
    # 4) Render & write config
    from app.printers import write_configs
    write_configs(
        config_tree=dhcp_tree, 
        template_name=template_name,
        template_dir=template_dir, 
        output_dir=out_path
    )
