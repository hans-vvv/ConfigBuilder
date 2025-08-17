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
