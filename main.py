from meraki_info import MerakiApiManager, MerakiExcelExporter
from config_generator import ConfigGenerator
from credentials import API_KEY


def main():

    manager = MerakiApiManager()
    manager.initialize(api_key=API_KEY)

    routes = manager.get_structured_static_routes()

    # exporter = MerakiExcelExporter(routes)
    # exporter.export_to_excel("meraki_static_routes.xlsx")

    config_generator = ConfigGenerator(use_cache=True)
    config_generator.set_api_data("static_routes", routes)
    config_generator.initialize("meraki_dhcp_info.xlsx")
    config_generator.write_configs()


if __name__ == "__main__":
    main()
