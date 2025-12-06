"""Internal module for downloading and caching PDB structures."""

import os
import tempfile
import urllib.error
import urllib.request
from pathlib import Path


def get_cache_dir() -> Path:
    """Get or create the PDB cache directory.

    Creates ~/.cache/mmdf/pdb if it doesn't exist.

    Returns
    -------
    Path
        Path to cache directory

    Raises
    ------
    PermissionError
        If cache directory cannot be created due to permissions
    """
    cache_dir = Path.home() / ".cache" / "mmdf" / "pdb"
    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        raise PermissionError(
            f"Cannot create cache directory at {cache_dir}. "
            f"Please check file system permissions."
        ) from e
    return cache_dir


def validate_pdb_id(pdb_id: str) -> str:
    """Validate and normalize a PDB ID.

    Supports both legacy 4-character and extended 12-character formats.
    Legacy format: 4 alphanumeric characters (e.g., "1abc", "7BQR")
    Extended format: 12 chars = "pdb_" + 8 alphanumeric (e.g., "pdb_00001abc", "pdb_00006UV8")

    Parameters
    ----------
    pdb_id : str
        The PDB ID to validate

    Returns
    -------
    str
        Normalized PDB ID (lowercase, whitespace stripped)

    Raises
    ------
    ValueError
        If PDB ID format is invalid

    Examples
    --------
    >>> validate_pdb_id("1ABC")
    '1abc'
    >>> validate_pdb_id("  1abc  ")
    '1abc'
    >>> validate_pdb_id("pdb_00001abc")
    'pdb_00001abc'
    >>> validate_pdb_id("PDB_00006UV8")
    'pdb_00006uv8'
    """
    pdb_id = pdb_id.strip().lower()

    # Check if it's a valid PDB ID format
    if len(pdb_id) == 4:
        # Legacy 4-character format
        if not pdb_id.isalnum():
            raise ValueError(
                f"Invalid PDB ID: '{pdb_id}'. "
                f"4-character PDB IDs must be alphanumeric."
            )
    elif len(pdb_id) == 12 and pdb_id.startswith("pdb_"):
        # Extended 12-character format: pdb_XXXXXXXX
        if pdb_id[3] != '_':
            raise ValueError(
                f"Invalid PDB ID: '{pdb_id}'. "
                f"Extended PDB IDs must include underscore: 'pdb_XXXXXXXX'."
            )
        if not pdb_id[4:].isalnum():
            raise ValueError(
                f"Invalid PDB ID: '{pdb_id}'. "
                f"Extended PDB IDs must be 'pdb_' followed by 8 alphanumeric characters."
            )
    else:
        raise ValueError(
            f"Invalid PDB ID: '{pdb_id}'. "
            f"PDB IDs must be either:\n"
            f"  - 4 alphanumeric characters (e.g., '1abc')\n"
            f"  - 12 characters 'pdb_XXXXXXXX' (e.g., 'pdb_00001abc')"
        )

    return pdb_id


def get_cached_file_path(pdb_id: str) -> Path:
    cache_dir = get_cache_dir()
    return cache_dir / f"{pdb_id}.cif"


def download_pdb(pdb_id: str, output_path: Path) -> None:
    """Download a PDB structure in mmCIF format from RCSB."""
    url = f"https://files.rcsb.org/download/{pdb_id}.cif"

    # Download to temporary file first for atomic operation
    tmp_fd, tmp_path_str = tempfile.mkstemp(
        dir=output_path.parent, suffix=".tmp", prefix=f"{pdb_id}_"
    )
    tmp_path = Path(tmp_path_str)

    try:
        # Close the file descriptor, we just need the path
        os.close(tmp_fd)

        # Download to temp file
        urllib.request.urlretrieve(url, tmp_path)

        # Atomic rename to final location
        tmp_path.rename(output_path)

    except urllib.error.HTTPError as e:
        tmp_path.unlink(missing_ok=True)
        if e.code == 404:
            raise FileNotFoundError(
                f"PDB entry '{pdb_id}' not found at {url}. "
                f"Please check that the PDB ID is correct."
            ) from e
        else:
            raise OSError(
                f"HTTP error {e.code} downloading PDB entry '{pdb_id}' from {url}"
            ) from e
    except urllib.error.URLError as e:
        tmp_path.unlink(missing_ok=True)
        raise OSError(
            f"Network error downloading PDB entry '{pdb_id}': {e.reason}"
        ) from e
    except Exception:
        # Clean up temp file on any other error
        tmp_path.unlink(missing_ok=True)
        raise


def fetch_pdb(pdb_id: str) -> Path:
    """Get a PDB structure from cache or download it."""
    # Validate and normalize PDB ID
    normalized_id = validate_pdb_id(pdb_id)

    # Check if already cached
    cached_path = get_cached_file_path(normalized_id)
    if cached_path.exists():
        return cached_path

    # Download and cache
    download_pdb(normalized_id, cached_path)

    return cached_path
