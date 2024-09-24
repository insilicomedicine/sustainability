import numpy as np
import pandas as pd
import os
import argparse

naming_dictionary = {
    "CO2_N2_selectivity_": "CO2/N2_selectivity",
    "CO2_uptake_P0.10bar_T363K__mmol_g_": "CO2_uptake_P0.10bar_T363K [mmol/g]",
    "CO2_uptake_P0.15bar_T298K__mmol_g_": "CO2_uptake_P0.15bar_T298K [mmol/g]",
    "heat_adsorption_CO2_P0.10bar_T363K__kcal_mol_": "heat_adsorption_CO2_P0.10bar_T363K [kcal/mol]",
    "heat_adsorption_CO2_P0.15bar_T298K__kcal_mol_": "heat_adsorption_CO2_P0.15bar_T298K [kcal/mol]",
    "heat_adsorption_N2_binary_P0.85bar_T298K__kcal_mol_": "heat_adsorption_N2_binary_P0.85bar_T298K [kcal/mol]",
    "N2_binary_uptake_P0.85bar_T298K__mmol_g_": "N2_binary_uptake_P0.85bar_T298K [mmol/g]",
    "working_capacity_vacuum_swing__mmol_g_": "working_capacity_vacuum_swing [mmol/g]",
    "bandgap": "Bandgap",
    "h2_uptake": "H2 uptake [mmol/g]",
    # Additional properties from ARC-MOF and MOFXDB
    "Ar_uptake_T87K_0.001pbar": "Ar_uptake_P0.001bar_T87K [mmol/g]",
    "CH4_uptake_T298K_0.05pbar": "CH4_uptake_P0.05bar_T298K [mmol/g]",
    "CH4_uptake_T338K_0.01pbar": "CH4_uptake_P0.01bar_T338K [mmol/g]",
    "CH4_uptake_T338K_4.4pbar": "CH4_uptake_P4.4bar_T338K [mmol/g]",
    "CO2_uptake_T298K_0.0004pbar": "CO2_uptake_P0.0004bar_T298K [mmol/g]",
    "CO2_uptake_T298K_0.01pbar": "CO2_uptake_P0.01bar_T298K [mmol/g]",
    "CO2_uptake_T298K_0.15pbar": "CO2_uptake_P0.15bar_T298K [mmol/g]",
    "CO2_uptake_T298K_0.1pbar": "CO2_uptake_P0.1bar_T298K [mmol/g]",
    "CO2_uptake_T313K_0.0004pbar": "CO2_uptake_P0.0004bar_T313K [mmol/g]",
    "CO2_uptake_T338K_0.0004pbar": "CO2_uptake_P0.0004bar_T338K [mmol/g]",
    "H2_uptake_T229K_1.0pbar": "H2_uptake_P1.0bar_T229K [mmol/g]",
    "H2_uptake_T313K_0.0004pbar": "H2_uptake_P0.0004bar_T313K [mmol/g]",
    "H2_uptake_T313K_0.6pbar": "H2_uptake_P0.6bar_T313K [mmol/g]",
    "H2_uptake_T313K_24.0pbar": "H2_uptake_P24.0bar_T313K [mmol/g]",
    "H2_uptake_T77K_0.0004pbar": "H2_uptake_P0.0004bar_T77K [mmol/g]",
    "H2_uptake_T77K_1.0pbar": "H2_uptake_P1.0bar_T77K [mmol/g]",
    "N2_uptake_T298K_0.75pbar": "N2_uptake_P0.75bar_T298K [mmol/g]",
    "N2_uptake_T298K_0.9pbar": "N2_uptake_P0.9bar_T298K [mmol/g]",
    "Xe_uptake_T298K_1.0pbar": "Xe_uptake_P1.0bar_T298K [mmol/g]",
    "wc_landfill-CO2": "working_capacity_landfill_CO2 [mmol/g]",
    "wc_pre_comb_4040-H2": "working_capacity_pre_combustion_4040_H2 [mmol/g]"
}

parser = argparse.ArgumentParser()
parser.add_argument("--output_dir", default="output_predictions", help="Folder with predictions")
parser.add_argument("--merged_results_path", default="merged_results.csv", help="Path to `.csv` file with merged results")

args = parser.parse_args()
output_dir = args.output_dir
merged_results_path = args.merged_results_path

property_dirs = os.listdir(output_dir)
if len(property_dirs) < 1:
    print("No folders are found in the provided directory.")
    raise SystemExit(1)

csv_pd_dict = {}
for property_dir in property_dirs:
    if property_dir in naming_dictionary.keys():
        csv_pd_dict[property_dir] = pd.read_csv(os.path.join(output_dir, property_dir, "test_prediction.csv"))

for property, csv_pd in csv_pd_dict.items():
    csv_pd_dict[property] = csv_pd_dict[property].drop(columns=['regression_labels'])
    csv_pd_dict[property] = csv_pd_dict[property].rename(columns={"regression_logits": naming_dictionary[property] if property in naming_dictionary.keys() else property})
    
merged_pd = list(csv_pd_dict.values())[0]
for csv_pd in list(csv_pd_dict.values())[1:]:
    merged_pd = pd.merge(merged_pd, csv_pd, 'outer', 'cif_id')
    
merged_pd = merged_pd.rename(columns={"cif_id": "CIF"})
merged_pd.to_csv(merged_results_path, index=False)
