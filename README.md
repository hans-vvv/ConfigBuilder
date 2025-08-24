# # Overview
I have run network projects for enterprises and service providers for 20+ years. In recent years I’ve been building automation scripts in Python to solve all kinds of problems. My experience so far is that data sources are mostly really messy or complex to interper and therefor custom scripting remains nessesary. This is my first attempt to build my personal toolkit and to solve problems in a structured way. I have added some real realistic challenges to demo how the tool can be used.

The tool is leveraging the Model-View-Controller (MVC) architecture, therefore provides a clean, scalable, and maintainable solution. Using MVC allows the project to organize core functionalities into separate modules and folders—making it easy to extend, maintain, and build new features without entangling business logic, data handling, and presentation layers.

---

## What This Demo Offers

- **Meraki API Integration:**  
  Connects to the Meraki cloud using the official Meraki Python SDK to fetch static routes and DHCP server data. This data is efficiently transformed into pandas DataFrames for flexible processing.

- **Data Transformation from Excel files:**  
  Reads and interprets network-related data from Excel, converting them into pandas DataFrames supported by the rest of the system.

- **Config Generation via Templates:**  
  Uses Jinja2 templating to generate network configuration files from easily consumable data structures, making it straightforward to create vendor-specific configs. The heavy lifting to achvieve is done in Python code.

- **Network CLI Parser:**  
  Parses CLI-based network configurations, transforming them into nested Python dictionaries for further automation or conversion, powered by a [specialized parsing module](https://github.com/tdorssers/confparser).

- **Golden comparison:**
  The tool runs with known input data and the generated configuration is compared against a stored “golden” output. This guarantees deterministic results and makes changes immediately visible as a text diff, so it’s clear whether an update is intentional or an unintended side-effect.

---

## Project Architecture and Views

The MVC-based architecture shines through in the project’s use of *Views*: modular components that encapsulate specific business logic combined with data, producing tailored outputs or configurations. 

---

TO DO:
- Finish demo views (high)
- Exception handling (high)
- Doc strings plus annotations everywhere (high)
- PyPi (medium)
- Gui (medium)
- Logging (medium)


