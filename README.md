# # Overview
I have run network projects for enterprises and service providers for 20+ years. In recent years I’ve been building automation scripts in Python to solve all kinds of problems. My experience so far is that data sources are mostly really messy or complex to interper and therefor custom scripting remains nessesary. This is my first attempt to build my personal toolkit and to solve problems in a structured way. I have added some real realistic challenges to demo how the tool can be used.

The tool is leveraging the Model-View-Controller (MVC) architecture, therefore provides a clean, scalable, and maintainable solution. Using MVC allows the project to organize core functionalities into separate modules and folders—making it easy to extend, maintain, and build new features without entangling business logic, data handling, and presentation layers.

---

## Demos

- [**Meraki API Integration:**](app/demos/meraki_api_integration/README.md):
  Connects to the Meraki cloud using the official Meraki Python SDK to fetch static routes and DHCP server data. This is supplemented with normalized data from an Excel file. 

- [**Network CLI Parser:**](app/demos/network_cli_parser/README.md): 
  Parses CLI-based network configurations, transforming them into nested Python dictionaries for further automation or conversion, powered by a [specialized parsing module](https://github.com/tdorssers/confparser).

- [**Golden Comparison:**](app/demos/golden_comparison/README.md):
  The tool runs with known input data and the generated configuration is compared against a stored “golden” output. This guarantees deterministic results and makes changes immediately visible as a text diff, so it’s clear whether an update is intentional or an unintended side-effect.


TO DO:
- Exception handling (high)
- Doc strings plus annotations everywhere (high)
- PyPi (medium)
- Gui (medium)
- Logging (medium)


