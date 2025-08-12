from meraki_info import MerakiInfo

def main():

    meraki_info = MerakiInfo()
    meraki_info.print_fixed_ip_assignments_to_excel_tab('Static bindings')
    meraki_info.print_reserved_ip_ranges_to_excel_tab('Reserved ranges')
    meraki_info.print_static_routes_to_excel_tab('Static routes')


if __name__ == "__main__":
    main()


