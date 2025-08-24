# TODO(medium): Add dataclasses (or pydantic models) for subtree payloads (e.g., DhcpSubnetConfig)
# to get editor-time and runtime validation.
from __future__ import annotations  # noqa: F401
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class StaticRoute:   
    network_name: str
    subnet_name: str
    subnet: str    
    enabled: bool
    fixed_ip_assignments: Optional[dict] = field(default_factory=dict)
    reserved_ip_ranges: Optional[list] = field(default_factory=list)
    comment: Optional[str] = None
    
