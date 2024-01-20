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
