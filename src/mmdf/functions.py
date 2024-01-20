"""functions provided by the package."""
import os

import gemmi
import pandas as pd

from ._gemmi_utils import structure_to_df


def read(filename: os.PathLike) -> pd.DataFrame:
    """Read a macromolecular structure file into a pandas DataFrame."""
    structure = gemmi.read_structure(str(filename))
    return structure_to_df(structure)
