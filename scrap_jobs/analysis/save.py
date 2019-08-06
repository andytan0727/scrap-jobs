"""
This module contains function to save scrapped data into local file system
"""

import os

from pandas import DataFrame


def save_to_csv(df: DataFrame, filename: str) -> None:
    """Save dataframe as csv file in data/ folder

    Args:
        df (DataFrame): Pandas DataFrame instance

        filename (str): Filename of the new file
    """
    if not isinstance(df, DataFrame):
        raise TypeError('Argument 1 must be an instance of pandas DataFrame.')

    save_path = os.path.join(os.path.curdir, 'data', filename)
    df.to_csv(save_path)


def save_to_excel(df: DataFrame, filename: str) -> None:
    """Save dataframe as excel file in data/ folder

    Args:
        df (DataFrame): Pandas DataFrame instance

        filename (str): Filename of the new file
    """
    if not isinstance(df, DataFrame):
        raise TypeError('Argument 1 must be an instance of pandas DataFrame.')

    save_path = os.path.join(os.path.curdir, 'data', filename)
    df.to_excel(save_path)
