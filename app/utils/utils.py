# TODO(medium): Add docstrings + type annotations to all helpers; promote shared DF utilities (safe_merge, coalesce).
import importlib
import inspect
import sys
from pathlib import Path
# from dataclasses import fields

import pandas as pd


# def read_excel_to_df(
#     wb_path: str | Path,
#     sheet_name: str,
#     fields: dict[str, str] | None = None
# ) -> pd.DataFrame:
#     """
#     Read Excel file into DataFrame.
#     - wb_path: absolute path to Excel file
#     - sheet_name: Excel sheet to read
#     - fields: optional mapping of original column names -> new column name
#     """
#
#     wb_path = Path(wb_path).resolve()
#     if not wb_path.exists():
#         raise FileNotFoundError(f"Excel file not found: {wb_path}")
#
#     df = pd.read_excel(wb_path, sheet_name=sheet_name, dtype=str)
#
#     # normalize headers
#     df.columns = df.columns.str.strip()
#
#     if fields:
#         df = df.rename(columns=fields)              # rename first
#         df = df[list(fields.values())]              # then select only wanted cols
#
#     return df


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


def create_excel_from_models(module_package_path: str, excel_output_path: str | Path) -> None:
    """
    Import a Python module by its package path, extract class dataclasses, and create an Excel workbook 
    with sheets for each class and columns for attributes.

    Args:
        module_package_path (str): Python import path to the models module (e.g. 'app.models.excel_models.dhcp_info_model').
        excel_output_path (str | Path): Absolute path where the Excel file will be saved.
    """
    excel_output_path = Path(excel_output_path).resolve()   
    
    top_level_dir = Path(__file__).parent
    # try to locate project root containing top-level package
    # Adjust this as per your project structure:
    project_root = top_level_dir.parent.parent   # adjust accordingly
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    # Import the module by package path
    models_module = importlib.import_module(module_package_path)

    with pd.ExcelWriter(excel_output_path, engine='xlsxwriter') as writer:
        for name, obj in inspect.getmembers(models_module, inspect.isclass):
            # Only consider classes defined in this module
            if obj.__module__ == models_module.__name__:
                annotations = getattr(obj, '__annotations__', {})
                if not annotations:
                    continue
                columns = list(annotations.keys())
                df = pd.DataFrame(columns=columns)
                df.to_excel(writer, sheet_name=name, index=False)
