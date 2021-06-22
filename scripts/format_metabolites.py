def main():
    import sys
    import os
    import numpy as np
    import pandas as pd
    
    file_input = sys.argv[1]

    compartment_dict = {
        "c":"dcs:CellularCompartmentEnumCytosol",
        "s": "dcs:CellularCompartmentEnumExtracellular",
        "l": "dcs:CellularCompartmentEnumLysosome",
        "r": "dcs:CellularCompartmentEnumEndoplasmicReticulum",
        "m": "dcs:CellularCompartmentEnumMitochondria",
        "p": "dcs:CellularCompartmentEnumPeroxisome",
        "g": "dcs:CellularCompartmentEnumGolgiApparatus",
        "n": "dcs:CellularCompartmentEnumNucleus",
        "c_i": "dcs:CellularCompartmentEnumInnerMitochondria"
    }

    df_metabolites = pd.read_csv(file_input, sep = "\t")
    # Remove metabolites with no chemicalFormula
    df_metabolites = df_metabolites[~pd.isna(df_metabolites["chemicalFormula"])]
    # modify id to humanGEMID format
    df_metabolites["id"] = df_metabolites["id"].str[2:]
    # Create new column for dcid
    df_metabolites["dcid"] = df_metabolites["chembl"]
    # use chemcialFormula as dcid if chemblID is not available
    df_metabolites["dcid"] = df_metabolites["dcid"].fillna(df_metabolites["chemicalFormula"])
    # use chemcialFormula as dcid if chemblID is not available
    df_metabolites["dcid"] = df_metabolites["dcid"].fillna(df_metabolites["id"])
    # format dcid -> bio/
    df_metabolites["dcid"] = "bio" + "/" + df_metabolites["dcid"].str.replace(":","")
    # Format chemblID, remove ":"
    df_metabolites["chembl"] = df_metabolites["chembl"].str.replace(":","")
    #convert chebiID and chemicalName to string with quotation
    df_metabolites['chebi'] = np.where(pd.isnull(df_metabolites['chebi']),df_metabolites['chebi']                                    ,'"' + df_metabolites['chebi'].astype(str) + '"')
    df_metabolites['name'] = np.where(pd.isnull(df_metabolites['name']),df_metabolites['name']                                    ,'"' + df_metabolites['name'].astype(str) + '"')
    # Pubchem Compound float -> int 
    df_metabolites["pubchem.compound"] = df_metabolites["pubchem.compound"].fillna(-1)
    df_metabolites["pubchem.compound"] = df_metabolites["pubchem.compound"].astype(int)
    df_metabolites["pubchem.compound"] = df_metabolites["pubchem.compound"].astype(str)
    df_metabolites["pubchem.compound"] = df_metabolites["pubchem.compound"].replace('-1', np.nan)
    # modify compartment to Enum type
    df_metabolites["compartment"] = df_metabolites["compartment"].map(compartment_dict)

    output_path = os.path.join(os.getcwd(), "metabolites.csv")
    df_metabolites.to_csv(output_path, index = None)

if __name__ == '__main__':
    main()


