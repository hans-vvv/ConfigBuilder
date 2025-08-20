from jinja2 import Environment, FileSystemLoader, StrictUndefined
from pathlib import Path


def get_jinja_env(templates_dir: str | Path | None = None) -> Environment:
    """
    Create and return a shared Jinja2 environment.
    - Templates must be in app/templates/
    """
    if templates_dir is None:
        templates_dir = Path(__file__).parent / "templates"
    else:
        templates_dir = Path(templates_dir)

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