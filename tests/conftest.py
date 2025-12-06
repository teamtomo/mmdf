from pathlib import Path

import pytest


@pytest.fixture
def test_data_directory() -> Path:
    return Path(__file__).parent.parent / "test_data"


@pytest.fixture
def test_pdb_file(test_data_directory) -> Path:
    return test_data_directory / "4v6x.cif"


@pytest.fixture
def test_output_file(test_data_directory) -> Path:
    return test_data_directory / "test_output.pdb"


@pytest.fixture
def mock_pdb_cache(tmp_path, monkeypatch):
    """Use temporary directory as PDB cache for testing."""
    cache_dir = tmp_path / "pdb_cache"
    cache_dir.mkdir()

    def mock_get_cache_dir():
        return cache_dir

    monkeypatch.setattr("mmdf._pdb_download.get_cache_dir", mock_get_cache_dir)

    return cache_dir
