import pickle
from typing import Any
from pathlib import Path


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
            return None

    def save(self, name: str, data: Any) -> None:
        path = self._path(name)
        with path.open("wb") as f:
            pickle.dump(data, f)
