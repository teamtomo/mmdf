"""functions provided by the package."""

import os

import gemmi
import pandas as pd

from ._gemmi_utils import df_to_structure, structure_to_df
from ._pdb_utils import fetch_pdb


def read(file_or_pdb_id: os.PathLike | str) -> pd.DataFrame:
    """Read a macromolecular structure into a pandas DataFrame.

    Parameters
    ----------
    file_or_pdb_id : os.PathLike
        Path to structure file, or PDB ID in format "pdb:<pdb_id>"
        (e.g., "pdb:1abc" to download from PDB)

    Returns
    -------
    pd.DataFrame
        DataFrame containing structure data

    Examples
    --------
    Read from local file:
    >>> df = mmdf.read("structure.cif")

    Download from PDB (legacy 4-char ID):
    >>> df = mmdf.read("pdb:1abc")

    Download from PDB (extended 12-char ID):
    >>> df = mmdf.read("pdb:pdb_00001abc")
    """
    filename_str = str(file_or_pdb_id)

    # Check for PDB ID format (case-insensitive)
    if filename_str.lower().startswith("pdb:"):
        pdb_id = filename_str[4:].strip()
        filepath = str(fetch_pdb(pdb_id))
    else:
        filepath = filename_str

    structure = gemmi.read_structure(filepath)
    return structure_to_df(structure)


def write(
    filename: os.PathLike,
    df: pd.DataFrame,
    pdb_write_options: gemmi.PdbWriteOptions = None,
) -> None:
    """Write a pandas DataFrame to a macromolecular structure file.

    Parameters
    ----------
    filename (os.PathLike): The file to write the DataFrame to.
    df (pd.DataFrame): The reference DataFrame containing the structure data.
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
