# # ConfigBuilder

ConfigBuilder is a practical Python application designed to address common challenges faced by network engineers. By leveraging the Model-View-Controller (MVC) architecture, this project provides a clean, scalable, and maintainable solution for managing complex network configuration tasks.

Using MVC allows the project to organize core functionalities into separate modules and folders—making it easy to extend, maintain, and build new features without entangling business logic, data handling, and presentation layers.

---

## What This Project Offers

- **Meraki API Integration:**  
  Connects to the Meraki cloud using the official Meraki Python SDK to fetch static routes and DHCP server data. This data is efficiently transformed into pandas DataFrames for flexible processing.

- **Data Transformation from Files:**  
  Reads and interprets network-related data from Excel or CSV files, converting them into pandas DataFrames supported by the rest of the system.

- **Config Generation via Templates:**  
  Uses Jinja2 templating to generate network configuration files from simplified, easily consumable data structures, making it straightforward to create vendor-specific configs.

- **Network CLI Parser:**  
  Parses CLI-based network configurations, transforming them into nested Python dictionaries for further automation or conversion, powered by a specialized parsing library.

---

## Project Architecture and Views

The MVC-based architecture shines through in the project’s use of *Views*: modular components that encapsulate specific business logic combined with data, producing tailored outputs or configurations.

Currently included views:

- **DHCP Server View:**  
  Generates FortiGate DHCP server configurations by combining live Meraki API data with supplementary template data from Excel files.

- **FortiGate Parser View:**  
  Converts FortiGate CLI configurations into ISC DHCP server configurations, enabling integration and migration between platforms.

---

TO DO:
- Finish demo views (high)
- Exception handling (high)
- Refactor printer to support printing of multiple view results (high)
- Doc strings plus annotations everywhere (high)
- PyPi (medium)
- Gui (medium)
- Tests (medium)
- Logging (medium)


