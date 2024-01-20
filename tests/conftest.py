from pathlib import Path

import pytest


@pytest.fixture
def test_data_directory() -> Path:
    return Path(__file__).parent.parent / "test_data"


@pytest.fixture
def test_pdb_file(test_data_directory) -> Path:
    return test_data_directory / "4v6x.cif"
