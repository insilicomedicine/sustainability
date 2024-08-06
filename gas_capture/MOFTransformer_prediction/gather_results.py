import numpy as np
import pandas as pd
import os
import argparse

naming_dictionary = {
    "CO2_N2_selectivity_": "CO2/N2_selectivity",
    "CO2_uptake_P0.10bar_T363K_": "CO2_uptake_P0.10bar_T363K [mmol/g]",
    "CO2_uptake_P0.15bar_T298K_": "CO2_uptake_P0.15bar_T298K [mmol/g]",
    "heat_adsorption_CO2_P0.10bar_T363K_": "heat_adsorption_CO2_P0.10bar_T363K [kcal/mol]",
    "heat_adsorption_CO2_P0.15bar_T298K_": "heat_adsorption_CO2_P0.15bar_T298K [kcal/mol]",
    "heat_adsorption_N2_binary_P0.85bar_T298K_": "heat_adsorption_N2_binary_P0.85bar_T298K [kcal/mol]",
    "N2_binary_uptake_P0.85bar_T298K_": "N2_binary_uptake_P0.85bar_T298K [mmol/g]",
    "working_capacity_vacuum_swing_": "working_capacity_vacuum_swing [mmol/g]"
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
    csv_pd_dict[property] = csv_pd_dict[property].rename(columns={"regression_logits": naming_dictionary[property]})
    
merged_pd = list(csv_pd_dict.values())[0]
for csv_pd in list(csv_pd_dict.values())[1:]:
    merged_pd = pd.merge(merged_pd, csv_pd, 'outer', 'cif_id')
    
merged_pd = merged_pd.rename(columns={"cif_id": "CIF"})
merged_pd.to_csv(merged_results_path, index=False)
