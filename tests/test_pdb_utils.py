"""Tests for PDB download and caching functionality."""

import pytest

from mmdf._pdb_utils import (
    get_cache_dir,
    get_cached_file_path,
    fetch_pdb,
    validate_pdb_id,
)


@pytest.mark.parametrize(
    "input_id,expected",
    [
        ("1abc", "1abc"),
        ("1ABC", "1abc"),
        ("1AbC", "1abc"),
        ("  1abc  ", "1abc"),
    ],
)
def test_valid_4char_pdb_id(input_id, expected):
    """Test valid 4-character PDB IDs are normalized to lowercase."""
    assert validate_pdb_id(input_id) == expected


@pytest.mark.parametrize(
    "input_id,expected",
    [
        ("pdb_00001abc", "pdb_00001abc"),
        ("PDB_00006UV8", "pdb_00006uv8"),
        ("PdB_0000AbC1", "pdb_0000abc1"),
        ("  pdb_00001abc  ", "pdb_00001abc"),
    ],
)
def test_valid_12char_pdb_id(input_id, expected):
    """Test valid 12-character extended PDB IDs are normalized."""
    assert validate_pdb_id(input_id) == expected


@pytest.mark.parametrize(
    "invalid_id",
    [
        "1ab",  # too short (3 chars)
        "1abcd",  # invalid length (5 chars)
        "",  # empty
        "    ",  # whitespace only
        "pdb00001abc",  # missing underscore
        "pd_b00001abc",  # wrong underscore position
        "pdb_0000-abc",  # non-alphanumeric
        "pdb12345",  # old 8-char format
        "pdb_0001abc",  # invalid length (11 chars)
        "toolong123",  # too long
        "invalid",  # completely invalid
    ],
)
def test_invalid_pdb_id_format(invalid_id):
    """Test that invalid PDB IDs raise ValueError."""
    with pytest.raises(ValueError, match="Invalid PDB ID"):
        validate_pdb_id(invalid_id)


def test_cache_dir_exists():
    """Test that cache directory is created."""
    cache_dir = get_cache_dir()
    assert cache_dir.exists()
    assert cache_dir.is_dir()


def test_cache_dir_path():
    """Test that cache directory has expected path structure."""
    cache_dir = get_cache_dir()
    assert cache_dir.name == "pdb"
    assert cache_dir.parent.name == "mmdf"
    assert cache_dir.parent.parent.name == ".cache"


def test_cached_file_path_format():
    """Test that cached file path has correct format."""
    path = get_cached_file_path("1abc")
    assert path.name == "1abc.cif"
    assert "pdb" in str(path)
    assert path.suffix == ".cif"


def test_cached_file_path_different_ids():
    """Test that different PDB IDs get different paths."""
    path1 = get_cached_file_path("1abc")
    path2 = get_cached_file_path("2xyz")
    assert path1 != path2
    assert path1.name == "1abc.cif"
    assert path2.name == "2xyz.cif"


@pytest.mark.network
def test_download_valid_pdb():
    """Test downloading a real PDB entry (requires network)."""
    # Use a small, well-known structure
    result = fetch_pdb("1crn")
    assert result.exists()
    assert result.suffix == ".cif"
    assert result.stat().st_size > 0


@pytest.mark.network
def test_use_cached_file():
    """Test that cached files are reused (requires network)."""
    # First download
    result1 = fetch_pdb("1crn")
    mtime1 = result1.stat().st_mtime

    # Second call should use cache
    result2 = fetch_pdb("1crn")
    mtime2 = result2.stat().st_mtime

    assert result1 == result2
    assert mtime1 == mtime2  # File wasn't re-downloaded


@pytest.mark.network
def test_download_nonexistent_pdb():
    """Test error handling for non-existent PDB ID (requires network)."""
    with pytest.raises(FileNotFoundError, match="not found"):
        fetch_pdb("9999")


def test_cached_file_exists():
    """Test that if a file exists in cache, it's returned immediately."""
    # Create a fake cached file
    from mmdf._pdb_utils import get_cache_dir
    cache_dir = get_cache_dir()
    cached_file = cache_dir / "1abc.cif"
    cached_file.write_text("fake cif content")

    # Should return the cached file without trying to download
    result = fetch_pdb("1abc")
    assert result == cached_file
    assert result.read_text() == "fake cif content"
