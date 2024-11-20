"""functions provided by the package."""

import os

import gemmi
import pandas as pd

from ._gemmi_utils import df_to_structure, structure_to_df


def read(filename: os.PathLike) -> pd.DataFrame:
    """Read a macromolecular structure file into a pandas DataFrame."""
    structure = gemmi.read_structure(str(filename))
    return structure_to_df(structure)


def write(
    filename: os.PathLike,
    df: pd.DataFrame,
    structure_name: str = "",
    pdb_write_options: gemmi.PdbWriteOptions = None,
) -> None:
    """Write a pandas DataFrame to a macromolecular structure file.

    Parameters
    ----------
    filename (os.PathLike): The file to write the DataFrame to.
    df (pd.DataFrame): The reference DataFrame containing the structure data.
    structure_name (str): Optional name to assign to the structure. Defaults to
        an empty string.
    pdb_write_options (gemmi.PdbWriteOptions): Optional PdbWriteOptions object
        to control the output format. See the gemmi documentation for more
        details. Defaults to None.

    Returns
    -------
    None
    """
    if pdb_write_options is None:
        pdb_write_options = gemmi.PdbWriteOptions()

    structure = df_to_structure(df)
    structure.write_pdb(str(filename), pdb_write_options)
