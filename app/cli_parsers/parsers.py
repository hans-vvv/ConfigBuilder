from pathlib import Path
from .confparser import Dissector


def parse_fortigate_config(config_file_path: str | Path, dissector_file_path: str | Path) -> dict:
    """
    Parse a FortiGate style configuration file at the given path using a dissector YAML file.

    Args:
        config_file_path (str | Path): Absolute or relative path to the FortiGate config file.
        dissector_file_path (str | Path): Absolute or relative path to the dissector YAML.

    Returns:
        Nested dict representing the parsed config.
    """
    config_path = Path(config_file_path).expanduser().resolve()
    dissector_path = Path(dissector_file_path).expanduser().resolve()

    config_text = config_path.read_text(encoding='utf-8')

    dissector = Dissector.from_file(str(dissector_path))

    tree = dissector.parse_str(config_text, indent=4)

    return dict(tree)
