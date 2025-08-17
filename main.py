from app.views import build_dhcp_subtree
from app.config_printer import write_configs


def main():

    dhcp_subtree = build_dhcp_subtree()
    write_configs(dhcp_subtree, output_dir="output_configs")


if __name__ == "__main__":
    main()
