from app.views import build_dhcp_subtree
from app.config_printer import write_configs


def main():

    import os
    template_dir = r"app/config_printer/templates"

    print("Looking in:", os.path.abspath(template_dir))
    print("Files found:", os.listdir(template_dir))

    dhcp_subtree = build_dhcp_subtree()
    write_configs(dhcp_subtree, output_dir="output_configs")


if __name__ == "__main__":
    main()
