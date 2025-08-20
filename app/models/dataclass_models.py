# TODO(medium): Add dataclasses (or pydantic models) for subtree payloads (e.g., DhcpSubnetConfig)
# to get editor-time and runtime validation.

from typing import Optional
from dataclasses import dataclass, field


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

@dataclass
class DhcpInfo:
    network_name: str
    subnet_name: str
    gwip: str
    lease_time: int
    ns_templ: str
    dhcp_templ: str

@dataclass
class DhcpOptionTemplate:
    """
    Represents a DHCP option template.
    
    Attributes:
        template: Template identifier.
        c1, c2, c3, c4: Option codes.
        t1, t2, t3, t4: Option types.
        v1, v2, v3, v4: Option values.  
    """
    template: str
    c1: str
    t1: str
    v1: str
    c2: str
    t2: str
    v2: str
    c3: str
    t3: str
    v3: str
    c4: str
    t4: str
    v4: str

@dataclass
class NameServerTemplate:
    template: str
    name_servers: str

