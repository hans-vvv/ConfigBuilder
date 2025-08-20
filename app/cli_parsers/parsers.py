import os
from .confparser import Dissector


def parse_fortigate_config(config_text: str) -> dict:
    """
    Parse a FortiGate style configuration text and return a nested dictionary tree.

    Args:
        config_text: The raw FortiGate config as a single string.

    Returns:
        Nested dict representing the parsed config.
    """

    # Locate dissector YAML relative to this file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dissector_path = os.path.join(base_dir, 'templates', 'fortigate', 'fortigate_dissector.yaml')

    # Load the dissector from YAML file
    dissector = Dissector.from_file(dissector_path)

    # Parse the config text 4 space indentation
    tree = dissector.parse_str(config_text, indent=4)

    return dict(tree)  # convert Tree (dict subclass) to plain dict

