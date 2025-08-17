import json
import os
from typing import Dict, Any
from app.config_printer import jinja_env


def render_template(template_name: str, **kwargs: Dict[str, Any]) -> str:
    """
    Render a Jinja2 template into a string.
    """
    template = jinja_env.get_template(template_name)
    return template.render(**kwargs)


def render_config_for_subtree(subtree: dict) -> str:
    """
    Render configuration text for a given subtree.
    """
    return render_template("dhcp_subtree.txt", subtree=subtree)


def write_configs(config_tree: dict, output_dir: str = ".") -> None:
    """
    Generate and write configuration files for each network in the config tree.
    """
    os.makedirs(output_dir, exist_ok=True)

    for network_name, network_subtree in config_tree.items():

        if network_name != "BRUSSELS":
            continue

        # print(json.dumps(network_subtree, indent=4))

        config_text = render_config_for_subtree(network_subtree)
        # print(config_text)
        output_path = os.path.join(output_dir, f"{network_name}-config.txt")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(config_text)

        print(f"[OK] Wrote config for {network_name} -> {output_path}")
