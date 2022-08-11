# macromolecular dataframes (mmdf)

Macromolecular DataFrames (`mmdf`) is a small package for reading macromolecular structures into pandas dataframes.
The heavy lifting of reading structure files is done by [gemmi](https://gemmi.readthedocs.io/en/latest/).

## Usage

```ipython
import mmdf

df = mmdf.read('4v6x-ribo.cif')
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
