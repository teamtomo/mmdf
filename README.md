# MacroMolecular DataFrames (mmdf)

[![License](https://img.shields.io/pypi/l/mmdf.svg?color=green)](https://github.com/teamtomo/mmdf/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/mmdf.svg?color=green)](https://pypi.org/project/mmdf)
[![Python Version](https://img.shields.io/pypi/pyversions/mmdf.svg?color=green)](https://python.org)
[![CI](https://github.com/teamtomo/mmdf/actions/workflows/ci.yml/badge.svg)](https://github.com/teamtomo/mmdf/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/teamtomo/mmdf/branch/main/graph/badge.svg)](https://codecov.io/gh/teamtomo/mmdf)

**M**acro**M**olecular **D**ata**F**rames (`mmdf`) is a small package for reading and writing macromolecular structure files
(.pdb/.mmCIF) using pandas dataframes.

The heavy lifting of reading structure files is performed by [gemmi](https://gemmi.readthedocs.io/en/latest/).

## Usage

```ipython
import mmdf

# Read a PDBx/mmCIF file into a dataframe
df = mmdf.read('4v6x.cif')
df.head()
Out[3]: 
  model chain residue  residue_id  ...       z charge occupancy  b_isotropic
0     1    Az     ASN           3  ... -54.829      0       1.0         10.0
1     1    Az     ASN           3  ... -54.691      0       1.0         10.0
2     1    Az     ASN           3  ... -53.642      0       1.0         10.0
3     1    Az     ASN           3  ... -53.007      0       1.0         10.0
4     1    Az     ASN           3  ... -54.239      0       1.0         10.0
[5 rows x 13 columns]

# Other dataframe manipulation...

# Write dataframe to a PDBx/mmCIF file
mmdf.write('4v6x_new.cif', df)
```

You can also fetch structures by their PDB ID, they will be cached in your home directory.

```python
import mmdf

df = mmdf.read("pdb:1crn")
```

## Changelog

### v0.0.4 (05/12/25)
- add pdb download functionality

### v0.0.3 (12/12/24)
- added basic write functionality
- resolved gemmi 0.7.0 incompatibility issues

### v0.0.2 (20/01/24)
- added atomic properties to dataframe output
- added support for `Path` arguments in `mmdf.read()`
- moved to `pyproject.toml` based packaging

### v0.0.1
- first release