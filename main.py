# TODO(medium): Load env vars for paths/models once; wire a CLI (argparse/typer) to select which views to render.
# Example flags: --view dhcp --output out/ --use-cache

from app.views import build_dhcp_subtree
from app.config_printer import write_configs


def main():

    dhcp_subtree = build_dhcp_subtree()
    write_configs(dhcp_subtree, output_dir="output_configs")


if __name__ == "__main__":
    main()
