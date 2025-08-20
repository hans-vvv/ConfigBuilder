# TODO(medium): Add docstrings + type annotations to all helpers; promote shared DF utilities (safe_merge, coalesce).
import pandas as pd
from pathlib import Path


def read_excel_to_df(
    wb_path: str | Path,
    sheet_name: str,
    fields: dict[str, str] | None = None
) -> pd.DataFrame:
    """
    Read Excel file into DataFrame.
    - wb_path: absolute path to Excel file
    - sheet_name: Excel sheet to read
    - fields: optional mapping of original column names -> new column name
    """

    wb_path = Path(wb_path).resolve()
    if not wb_path.exists():
        raise FileNotFoundError(f"Excel file not found: {wb_path}")

    df = pd.read_excel(wb_path, sheet_name=sheet_name, dtype=str)

    # normalize headers
    df.columns = df.columns.str.strip()

    if fields:
        df = df.rename(columns=fields)              # rename first
        df = df[list(fields.values())]              # then select only wanted cols

    return df

def coalesce(*args):
    """
    Return the first argument that is not None, NaN, or an empty string.
    
    This helper is designed for use with pandas objects to simplify selection of the first valid value
    among multiple columns, typically after DataFrame merges where overlapping columns may contain NaNs.
    
    Args:
        *args: A variable number of values to check.

    Returns:
        The first value that is not None, not pandas.NaN, and not an empty string; otherwise None.
    """
    for arg in args:
        if arg is not None and pd.notna(arg) and arg != '':
            return arg
    return None
