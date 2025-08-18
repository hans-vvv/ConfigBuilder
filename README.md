# ConfigBuilder
This project builds FTG network configurations based on Excel or CSV template files and/or data fetched via
a Meraki API.

The project supports building the following configuration parts:
- DHCP server configuration
- . . .

TO DO:
- Exception handling (high)
- Refactor printer to support printing of multiple view results (high)
- Meraki API Cache using pickle (high)
- Doc strings plus annotations everywhere (high)
- Gui (medium)
- Tests (some, not all, maybe none unit, plus integration) (medium)
- Logging (medium)
- Environment variables (medium)
- Export project to PIP (medium)
- Type validation during runtime (low)
- Linter (low)
- . . .

“Implement the cache: Create .cache/meraki/static_routes.pkl and wire use_cache toggle in meraki_info.py. Add load_cache()/save_cache() and wrap API fetch.”

“Refactor printer: Update printer.py to accept a dict of view trees and render multiple templates per network in order: dhcp → interfaces → bgp.”

“Harden merges: In dhcp_view.py, add a small coalesce helper and normalize network_name, subnet after the join. Write tests.”

“Add logging: Insert logger.info statements showing row counts before/after each merge and when skipping rows without gwip.”

“Validate output: Define DhcpSubnetConfig pydantic model and validate each row before adding to dhcp_tree.”