# # Overview
The workflow to achieve the desired result of printing Fortigate DHCP server configurations based on data 
taken from the Meraki API and an Excel document is defined here. 


### Step 1: Create Model Files for Excel and Meraki API

You begin by defining data models representing both your Excel sheets and Meraki API structures.  
Key files:

- [Excel Models](../../models/excel_models/dhcp_info_model.py)  
- [Meraki API Models](../../models/api_models/meraki_models.py)  

### Step 2: Create empty Excel File based on the model spec.

Generate an empty Excel file based on your models.  
- Run the `print_empty_excel_based_on_models_specs.run()` function in [main.py](../../../main.py).
- You may need to comment out improper imports temporarily to run the correct `.run()` function.  
- The view file to accomplish this is [here](../../views/print_empty_excel_based_on_model_specs.py) 
- The result is stored [here](../../src/empty/dhcp_info_models.xlsx)

### Step 3: Fill in the Demo Data

Populate your Excel file with test data.  
- The filled in Excel file is located [here](../../src/mock_data/dhcp_info_mock.xlsx) 

### Step 4: Create Queries to Extract Needed Data

Build query classes to extract relevant data from the Excel sheets.
- See: [DHCP Info Queries](../../models/excel_models/dhcp_info_queries.py)
- Pandas library is used to join the normalized tables.

### Step 5: Create API Queries

Implement queries to fetch data from the Meraki API.  
- See: [Meraki API Queries](../../models/api_models/meraki_queries.py)  
- Mocked data is produced [here](../../src/mock_data/meraki_mock_data.py) 
- Pandas library is used here too.

### Step 6: Create View to Generate Fortigate DHCP Server Configurations

Create a view that combines normalized data from both Excel and API queries for configuration generation.  
- See: [View: test_create_ftg_dhcp_server_cfg.py](../../views/test_create_ftg_dhcp_server_cfg.py)  
- The two query instances returns normalized dicts that are merged into another dict.
- The purpose of this view is to facilitate the Golden Test. Therefor the name of the file is prefixed with test/.
- So the result is based on the test Excel file Meraki mocked data.
- The printer class uses Jinja2 library to render the configuration dict.
- The Jinja2 template can be found [here](../../templates/fortigate/dhcp_subtree.j2)

### Step 7: Print the configuration

Finally, the configuration can be printed.
- Run the `test_create_ftg_dhcp_server_cfg.run()` function in [main.py](../../../main.py).
- You may need to comment out improper imports temporarily to run the correct `.run()` function.
- The end result is printed [here](../../test_output_configs/brussels.cfg)

