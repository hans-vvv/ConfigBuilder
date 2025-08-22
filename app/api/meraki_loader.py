# TODO(medium): Validate Excel columns at load time; raise clear error if a required column is missing.
# Add a small schema map per sheet (name -> required columns).
import pickle
import pandas as pd

from typing import Any
from pathlib import Path

import meraki

import pandas as pd

from app.models import StaticRoute
from app.app_config.secrets import MERAKI_API_KEY


class MerakiCache:
    """Ultra-simple pickle cache: load/save by name under a cache_dir."""

    def __init__(self, cache_dir: str | Path = ".cache/meraki"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, name: str) -> Path:
        return self.cache_dir / f"{name}.pkl"

    def load(self, name: str) -> Any | None:
        path = self._path(name)
        if not path.exists():
            return None
        try:
            with path.open("rb") as f:
                return pickle.load(f)
        except Exception:
            # On any load error, ignore cache (acts like "miss")
            pass

    def save(self, name: str, data: Any) -> None:
        path = self._path(name)
        with path.open("wb") as f:
            pickle.dump(data, f)


class MerakiApiManager:

    def __init__(self):
        
        self.dashboard = None
        self.cache_controls = MerakiCache()                   

    def get_dashbord(self, api_key=MERAKI_API_KEY, print_console=False, suppress_logging=True):
        return meraki.DashboardAPI(
            api_key=api_key, print_console=print_console, suppress_logging=suppress_logging,
        ) 

get_meraki_api = MerakiApiManager()
