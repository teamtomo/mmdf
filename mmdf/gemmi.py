import gemmi
import pandas as pd


def structure_to_df(structure: gemmi.Structure) -> pd.DataFrame:
    dfs = []
    headings = [
        'model',
        'chain',
        'residue',
        'residue_id',
        'atom',
        'element',
        'heteroatom_flag',
        'x',
        'y',
        'z',
        'charge',
        'occupancy',
        'b_isotropic'
    ]
    for model in structure:
        data = [
            (
                model.name,
                cra.chain.name,
                cra.residue.name,
                cra.residue.seqid.num,
                cra.atom.name,
                cra.atom.element.name,
                cra.residue.het_flag,
                cra.atom.pos.x,
                cra.atom.pos.y,
                cra.atom.pos.z,
                cra.atom.charge,
                cra.atom.occ,
                cra.atom.b_iso
            )
            for cra
            in model.all()
        ]
        df = pd.DataFrame(data, columns=headings)
        dfs.append(df)
    return pd.concat(dfs)
