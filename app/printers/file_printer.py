# TODO(high): Refactor printer to accept multiple view outputs (e.g., dhcp_tree, bgp_tree, interfaces_tree)
# and render a single combined config per network. Consider a registry like:
#   def render_all(network_name: str, trees: dict[str, dict]) -> str
# Then iterate templates in a deterministic order.
import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader



def write_configs(
        config_tree: dict, 
        template_name: str, 
        output_dir: str = ".", 
        template_dir: str | Path | None = None
) -> None:
    """
    Generate and write configuration files for each network in the config tree.
    """
    # os.makedirs(output_dir, exist_ok=True)

    if template_dir is None:
        # Default to your known template path, adjust as needed
        template_dir = Path(__file__).parent.parent / "templates" / "fortigate"
    else:
        template_dir = Path(template_dir)
    
    
    env = Environment(loader=FileSystemLoader(str(template_dir)), trim_blocks=True, lstrip_blocks=True)    
    os.makedirs(output_dir, exist_ok=True)
    template = env.get_template(template_name)

    for network_name, network_subtree in config_tree.items():

        if network_name != "BRUSSELS":
            continue        

        config_text = template.render(subtree=network_subtree)
        output_path = Path(output_dir) / f"{network_name}-config.txt"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(config_text)
        print(f"[OK] Wrote config for {network_name} -> {output_path}")
