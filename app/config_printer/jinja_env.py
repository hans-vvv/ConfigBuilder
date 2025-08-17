from jinja2 import Environment, FileSystemLoader, StrictUndefined
from pathlib import Path


def get_jinja_env() -> Environment:
    """
    Create and return a shared Jinja2 environment.
    - Templates must be in app/config_printer/templates/
    """
    templates_dir = Path(__file__).parent / "templates"
    file_loader = FileSystemLoader(str(templates_dir))
    env = Environment(
        loader=file_loader,
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=StrictUndefined,  # error if variable is missing
    )
    env.add_extension("jinja2.ext.loopcontrols")

    # Example: custom filters can be added here
    # env.filters["upper"] = str.upper

    return env


jinja_env = get_jinja_env()