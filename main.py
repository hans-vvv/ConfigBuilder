from meraki_info import MerakiInfo
from config_generator import ConfigGenerator


def main():

    meraki_info = MerakiInfo(get_meraki_data=False)

    meraki_info.print_fixed_ip_assignments_to_excel_tab()
    meraki_info.print_reserved_ip_ranges_to_excel_tab()
    meraki_info.print_static_routes_to_excel_tab()

    config_generator = ConfigGenerator()
    config_generator.print_configs()


if __name__ == "__main__":
    main()
