# # Overview
This demo shows how you can quite easily extract data from a CLI block based configuration file. The source file we
are going to use is the file produced in the first demo.

### Step 1: Create dissector model file for Fortigate based configurations

Documentation plus sample examples for different vendors can be found [here](https://github.com/tdorssers/confparser) 
- The dissector file used in the example is found [here](../../templates/fortigate/fortigate_dissector.yaml)


### Step 2: Create view

The view will only print the result based on the dissector file and the configuration
- The view can be found [here](../../views/demo_parse_ftg_dhcp_server_cfg.py)
- The view will only print the result based on the dissector file and the configuration

### Step 3: Print result
Run the `demo_parse_ftg_dhcp_server_cfg.run()` function in [main.py](../../../main.py).
- You may need to comment out improper imports temporarily to run the correct `.run()` function.
- The result is printed to screen.
- I leave it to the reader to produce a new config from a different vendor based on the result.
