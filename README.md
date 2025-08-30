# # Overview

I have have participated in network projects for enterprises and service providers for over 20 years. In recent years, I’ve
been building automation scripts in Python to address a wide range of challenges. My experience so far is
that data sources are often messy or complex to interpret, and therefore custom scripting remains necessary.
This is my first attempt to build a personal toolkit to solve problems in a more structured way. I’ve also
included some realistic challenges to demonstrate how the tool can be used.

The tool leverages the Model-View-Controller (MVC) architecture, providing a clean, scalable, and
maintainable solution. Using MVC allows the project to separate core functionalities into distinct modules
and folders, making it easier to extend, maintain, and add new features without entangling business logic,
data handling, and presentation layers.

---

## Demos

- [**Meraki API Integration:**](app/demos/meraki_api_integration/README.md)
  Connects to the Meraki cloud using the official Meraki Python SDK to fetch static routes and DHCP server data. This is supplemented with normalized data from an Excel file. 

- [**Network CLI Parser:**](app/demos/network_cli_parser/README.md)
  Parses CLI-based network configurations, transforming them into nested Python dictionaries for further automation or conversion, powered by a [specialized parsing module](https://github.com/tdorssers/confparser).

- [**Golden Comparison:**](app/demos/golden_comparison/README.md)
  The tool runs with known input data and the generated configuration is compared against a stored “golden” output. This guarantees deterministic results and makes changes immediately visible as a text diff, so it’s clear whether an update is intentional or an unintended side-effect.
