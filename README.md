# MacroMolecular DataFrames (mmdf)

[![License](https://img.shields.io/pypi/l/mmdf.svg?color=green)](https://github.com/teamtomo/mmdf/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/mmdf.svg?color=green)](https://pypi.org/project/mmdf)
[![Python Version](https://img.shields.io/pypi/pyversions/mmdf.svg?color=green)](https://python.org)
[![CI](https://github.com/teamtomo/mmdf/actions/workflows/ci.yml/badge.svg)](https://github.com/teamtomo/mmdf/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/teamtomo/mmdf/branch/main/graph/badge.svg)](https://codecov.io/gh/teamtomo/mmdf)

**M**acro**M**olecular **D**ata**F**rames (`mmdf`) is a small package for reading macromolecular structure files
(.pdb/.mmCIF) into pandas dataframes.

The heavy lifting of reading structure files is performed by [gemmi](https://gemmi.readthedocs.io/en/latest/).

## Usage

```ipython
import mmdf

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
```
