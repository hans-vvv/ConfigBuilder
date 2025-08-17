import json

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

class Tree(dict):
    """ Autovivificious dictionary """

    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

    def __str__(self):
        """ Serialize dictionary to JSON formatted string with indents """
        return json.dumps(self, indent=4)
