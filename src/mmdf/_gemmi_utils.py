import gemmi
import pandas as pd

HEADINGS = [
    "model",
    "chain",
    "residue",
    "residue_id",
    "atom",
    "element",
    "atomic_number",
    "atomic_weight",
    "covalent_radius",
    "van_der_waals_radius",
    "heteroatom_flag",
    "x",
    "y",
    "z",
    "charge",
    "occupancy",
    "b_isotropic",
]


def structure_to_df(structure: gemmi.Structure) -> pd.DataFrame:
    dfs = []

    for model in structure:
        data = [
            (
                model.num,
                cra.chain.name,
                cra.residue.name,
                cra.residue.seqid.num,
                cra.atom.name,
                cra.atom.element.name,
                cra.atom.element.atomic_number,
                cra.atom.element.weight,
                cra.atom.element.covalent_r,
                cra.atom.element.vdw_r,
                cra.residue.het_flag,
                cra.atom.pos.x,
                cra.atom.pos.y,
                cra.atom.pos.z,
                cra.atom.charge,
                cra.atom.occ,
                cra.atom.b_iso,
            )
            for cra in model.all()
        ]
        df = pd.DataFrame(data, columns=HEADINGS)
        dfs.append(df)
    return pd.concat(dfs)


def df_to_structure(df: pd.DataFrame, structure_name: str = "") -> gemmi.Structure:
    """Helper function to convert a DataFrame to a gemmi.Structure."""
    # Check for the required columns
    required_columns = set(HEADINGS)
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        raise ValueError(f"Missing required columns: {missing}")

    structure = gemmi.Structure()
    structure.name = structure_name

    # Nested iteration over model, chain, residue, and atom to populate the
    # Structure object
    for _, model_df in df.groupby("model"):
        model = gemmi.Model(model_df["model"].iloc[0])

        for _, chain_df in model_df.groupby("chain"):
            chain = gemmi.Chain(chain_df["chain"].iloc[0])

            for _, residue_df in chain_df.groupby("residue_id"):
                residue = gemmi.Residue()
                residue.name = residue_df["residue"].iloc[0]
                residue.seqid.num = residue_df["residue_id"].iloc[0]
                residue.het_flag = residue_df["heteroatom_flag"].iloc[0]

                for _, atom_row in residue_df.iterrows():
                    atom = gemmi.Atom()
                    atom.name = atom_row["atom"]
                    atom.element = gemmi.Element(atom_row["element"])
                    atom.pos = gemmi.Position(
                        atom_row["x"], atom_row["y"], atom_row["z"]
                    )
                    atom.charge = atom_row["charge"]
                    atom.occ = atom_row["occupancy"]
                    atom.b_iso = atom_row["b_isotropic"]

                    residue.add_atom(atom)

                chain.add_residue(residue)

            model.add_chain(chain)

        structure.add_model(model)

    return structure
