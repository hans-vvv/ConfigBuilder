import json

import pandas as pd


def read_excel_to_df(filename: str, sheet_name: str, fields: dict[str, str]) -> pd.DataFrame:
    """
    Generic helper: read Excel sheet into a DataFrame with normalized headers
    and renamed columns based on `fields`.
    """
    df = pd.read_excel(
        filename,
        sheet_name=sheet_name,
        dtype=str
    )

    df.columns = df.columns.str.strip()       # normalize headers
    df = df.rename(columns=fields)            # rename
    df = df[list(fields.values())]            # select only wanted cols

    return df


class Tree(dict):
    """ Autovivificious dictionary """

    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

    def __str__(self):
        """ Serialize dictionary to JSON formatted string with indents """
        return json.dumps(self, indent=4)
