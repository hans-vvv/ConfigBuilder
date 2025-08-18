# TODO(medium): Load env vars for paths/models once; wire a CLI (argparse/typer) to select which views to render.
# Example flags: --view dhcp --output out/ --use-cache

from app.meraki_api import get_meraki_api
from app.views import DhcpView
from app.config_printer import write_configs


def main():

    meraki_api = get_meraki_api(use_cache=True)

    dhcp_view = DhcpView(meraki_api)
    dhcp_subtree = dhcp_view.build_dhcp_subtree()
    write_configs(dhcp_subtree, output_dir="output_configs")


if __name__ == "__main__":
    main()
