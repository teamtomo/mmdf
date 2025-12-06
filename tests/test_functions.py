import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    import pandas as pd

    import mmdf


def test_read(test_pdb_file):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        df = mmdf.read(test_pdb_file)
    assert isinstance(df, pd.DataFrame)


def test_write(test_pdb_file, test_output_file):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        df = mmdf.read(test_pdb_file)
        mmdf.write(test_output_file, df)

        assert test_output_file.exists()

        df2 = mmdf.read(test_output_file)

        assert isinstance(df2, pd.DataFrame)

    # Sort the dataframes by the chain column to ensure comparison
    df = df.sort_values(by="chain", kind="mergesort").reset_index(drop=True)
    df2 = df2.sort_values(by="chain", kind="mergesort").reset_index(drop=True)

    assert df.equals(df2)

    test_output_file.unlink()

def test_read_from_pdb_id():
    """Test reading with 'pdb:' prefix (lowercase)."""
    import pytest

    pytest.importorskip("mmdf")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        df = mmdf.read("pdb:1crn")
    assert isinstance(df, pd.DataFrame)
