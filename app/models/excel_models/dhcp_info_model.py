# TODO(medium): Add dataclasses (or pydantic models) for subtree payloads (e.g., DhcpSubnetConfig)
# to get editor-time and runtime validation.
from __future__ import annotations  # noqa: F401
from functools import lru_cache
from typing import Optional
from dataclasses import dataclass
from app.utils import load_all_excel_sheets

@dataclass
class DhcpInfo:
    network_name: str
    subnet_name: str
    gw_ip: str
    lease_time: int
    ns_template: Optional[NameServerTemplate] = None
    dhcp_option_template: Optional[DhcpOptionTemplate] = None


@dataclass
class DhcpOptionTemplate:
    template_name: str
    dhcp_options: list[DhcpOption]


@dataclass
class DhcpOption:
    id: int
    code: str
    type: str
    value: str
    

@dataclass
class NameServer:
    """
    Represents a single name server entity.
    """
    id: int                       # Unique identifier for the name server
    address: str                  # IP address or hostname of the name server
    description: str = ""         # Optional description


@dataclass
class NameServerTemplate:
    """
    Represents a name server template grouping multiple name servers.
    """
    template_name: str            # Identifier or name of the template
    name_servers: list[NameServer]  # List of associated name server objects


@lru_cache(maxsize=1)
def load_data(filepath: str):   
    return load_all_excel_sheets(filepath=filepath)

