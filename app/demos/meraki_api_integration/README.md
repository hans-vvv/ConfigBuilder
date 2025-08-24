# # Overview
The worflow to achieve the desired result of printing Fortigate based DHCP server configurations is defined here.


### Step 1: Create Model Files for Excel and Meraki API

You begin by defining data models representing both your Excel sheets and Meraki API structures.  
Key files:

- [Excel Models](../../models/excel_models/dhcp_info_model.py)  
- [Meraki API Models](../../models/api_models/meraki_models.py)  

### Step 2: Create empty Excel File based on the model spec.

Generate an empty Excel file based on your models.  
- Run the `print_empty_excel_based_on_models_specs.run()` function in [main.py](../../../main.py).  
- Note: You may need to comment out improper imports temporarily to run the correct `.run()` function.  

### Step 3: Fill in the Demo Data

Populate your Excel file with test data.  
- The filled in Excel file is located [here](../../src/test/dhcp_info_test.xlsx) 

### Step 4: Create Queries to Extract Needed Data

Build query classes to extract relevant data from the Excel sheets.
- See: [DHCP Info Queries](../../models/excel_models/dhcp_info_queries.py)
- Note: Pandas library is used to join normalized excel data

### Step 5: Create API Queries

Implement queries to fetch data from the Meraki API.  
- See: [Meraki API Queries](../../models/api_models/meraki_queries.py)  
- Note: Mocked data can be provided to facilitate Golden Tests.
- Note: Pandas library is used here too.

### Step 6: Create View to Generate Fortigate DHCP Server Configurations

Create a view that combines normalized data from both Excel and API queries for configuration generation.  
- See: [View: test_create_ftg_dhcp_server_cfg.py](../../views/test_create_ftg_dhcp_server_cfg.py)  
- Note: The two query instances loads normalized dictionaries that can be easily merged for configuration construction.
- Note: The printer class uses Jinja2 library to render the configuration dict.

