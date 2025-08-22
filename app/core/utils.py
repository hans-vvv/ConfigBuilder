# TODO(medium): Add docstrings + type annotations to all helpers; promote shared DF utilities (safe_merge, coalesce).
import os
import pandas as pd
from pathlib import Path
from typing import Type
from dataclasses import fields, is_dataclass


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


def generate_excel_template(filepath: str, dataclass_types: list[Type]) -> None:
    # Ensure parent directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
        for dc in dataclass_types:
            if not is_dataclass(dc):
                raise ValueError(f"{dc} is not a dataclass type")           
            
            col_names = [f.name for f in fields(dc)]
            df = pd.DataFrame(columns=col_names)
            df.to_excel(writer, sheet_name=dc.__name__, index=False)
    
    print(f"Excel template created at {filepath}")


def load_all_excel_sheets(filepath: str) -> dict[str, pd.DataFrame]:
    """
    Load all sheets from an Excel file into a dictionary of DataFrames.
    
    Args:
        filepath: Path to the Excel file.
    
    Returns:
        Dictionary where keys are sheet names and values are pandas DataFrames.
    """
    file_path = Path(filepath)
    excel_data = pd.read_excel(file_path, sheet_name=None)  # Load all sheets
    return excel_data  # Dict[str, DataFrame]


def find_project_root(start_path: Path | None = None) -> Path:
    """
    Traverse upwards from start_path (or current file location if None) until a directory
    containing '.git' is found. That directory is considered the project root.

    Args:
        start_path: The starting path to begin searching from.

    Returns:
        Path object pointing to the project root directory.

    Raises:
        RuntimeError: If no '.git' directory is found in any parent folders.
    """
    if start_path is None:
        start_path = Path(__file__).resolve()

    for parent in [start_path] + list(start_path.parents):
        if (parent / '.git').is_dir():
            return parent

    raise RuntimeError("Project root not found. Make sure to run inside a Git repository.")


def pprint_df(df: pd.DataFrame) -> None:
        """
        Pprint a pandas DataFrame 
        """         
        with pd.option_context(
            'display.max_columns', None,
            'display.max_rows', 20,
            'display.width', 1000,
            'display.colheader_justify', 'left'
        ):
            print(df)


def merge_nested_dicts(d1: dict, d2: dict) -> dict:
    """
    Recursively merge nested dictionaries d2 into d1.
    If keys overlap at inner dict level, update inner dict values.
    """
    for key, value in d2.items():
        if key in d1 and isinstance(d1[key], dict) and isinstance(value, dict):
            d1[key] = merge_nested_dicts(d1[key], value)
        else:
            d1[key] = value
    return d1
