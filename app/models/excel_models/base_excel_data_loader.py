from pathlib import Path
from typing import Optional, Dict
import pandas as pd
from app.utils import load_all_excel_sheets, find_project_root


class BaseExcelDataLoader:
    """
    Base class to load Excel sheets into DataFrames and provide access.
    """

    def __init__(self, excel_filepath: str | Path, auto_load: bool = True):
        filepath = Path(excel_filepath)
        if not filepath.is_absolute():
            project_root = find_project_root()
            filepath = project_root / filepath
        self.excel_filepath = filepath.resolve()
        self._dfs: Optional[Dict[str, pd.DataFrame]] = None
        if auto_load:
            self.load()

    def load(self) -> None:
        """Load all sheets into DataFrames."""
        self._dfs = load_all_excel_sheets(str(self.excel_filepath))

    def get_dataframe_from_sheet(self, sheetname: str) -> pd.DataFrame:
        """Get loaded DataFrame for the given sheet name."""
        if self._dfs is None:
            raise ValueError("Data not loaded yet; call load() first.")
        if sheetname not in self._dfs:
            raise ValueError(f"Sheet {sheetname} not found in loaded data.")
        return self._dfs[sheetname]

