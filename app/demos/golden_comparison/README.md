# # Overview
The goal is to verify if a produced configuration using test data from the first demo is equal to the "Golden" config
stored on disk.  I included integration tests to guarantee consistency, so changes can be made with confidence. 


### Step 1: Create golden_config script.

The script will produce the result of the comparison of running the test_* view and the Golden config.
- The script is located [here](../../../tests/dhcp/compare_golden.py)
- It is not located under the app directory, but under the tests directory.
- In the script the result from test_create_ftg_dhcp_server_cfg.py view is rendered in memory
- And this data is validated against the Golden Config.

### Step 2: Run golden_config script.

If there is no Golden config present in the "golden" directory (/tests/dhcp/golden) then when the script is run
it will create the golden config and it will place it into the directory.

> [ACCEPT] wrote dhcp\golden\BRUSSELS.conf

You can either accept it (do nothing) or reject it by removing it.

If you have accepted the golden config then you must run the script again if you want to compare.

If the produced result is equal to the golden config, the result is:
> [OK] matches golden: dhcp\golden\BRUSSELS.conf

If the produced result is not equal to the golden config, the result points where the difference is located:
> @@ -3,7 +3,7 @@
-        set interface "Interco_vlan920"
+        set interface "Interco_vlan930"

