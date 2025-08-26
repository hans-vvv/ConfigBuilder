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
- I leave it to the reader to produce a new config from a different vendor based on the result.

<div style="max-height: 300px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; font-family: monospace; background: #f9f9f9;">
<pre>
{
  "dhcp_server": {
    "scope": {
      "10": {
        "def_gw": "1.1.1.1",
        "netmask": "255.255.255.0",
        "interface": "\"Interco_vlan920\"",
        "ip-ranges": {
          "1": {
            "start_ip": "1.1.1.1",
            "end_ip": "1.1.1.254"
          }
        },
        "options": {
          "1": {
            "code": "c1",
            "type": "ip",
            "ip": "v1"
          },
          "2": {
            "code": "c2",
            "type": "t2",
            "value": "v2"
          }
        },
        "reserved_addresses": {
          "1": {
            "ip": "1.1.1.11",
            "type": "04:42:1a:c9:99:9b",
            "description": "\"test1\""
          },
          "2": {
            "ip": "1.1.1.12",
            "type": "04:42:1a:c9:c9:9b",
            "description": "\"test2\""
          }
        },
        "dns_servers": {
          "1.1.1.1": {},
          "1.0.1.0": {}
        }
      },
      "11": {
        "def_gw": "2.2.2.2",
        "netmask": "255.255.255.0",
        "interface": "\"Interco_vlan920\"",
        "ip-ranges": {
          "1": {
            "start_ip": "2.2.2.1",
            "end_ip": "2.2.2.254"
          }
        },
        "options": {
          "1": {
            "code": "c3",
            "type": "t3",
            "value": "v3"
          },
          "2": {
            "code": "c4",
            "type": "t4",
            "value": "v4"
          }
        },
        "reserved_addresses": {
          "1": {
            "ip": "2.2.2.11",
            "type": "05:42:1a:c9:99:9b",
            "description": "\"test3\""
          },
          "2": {
            "ip": "2.2.2.12",
            "type": "05:42:1a:c9:c9:9b",
            "description": "\"test4\""
          }
        },
        "dns_servers": {
          "8.8.4.4": {},
          "8.8.8.8": {}
        }
      }
    }
  }
}
</pre>
</div>
