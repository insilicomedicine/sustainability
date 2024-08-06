import numpy as np
import pandas as pd
import os
import json
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--cif_input_path", help="Path to the directory with input .cif files with simulation.json results.")
parser.add_argument("--merged_results_path", default="merged_results.csv", help="Path to `.csv` file with merged results")
args = parser.parse_args()
output_dir = Path(args.cif_input_path)
merged_results_path = args.merged_results_path

if "simulation_results.json" not in os.listdir(output_dir):
    print("simulation_results.json not found within the provided directory. Make sure that MOFDiff simulation has completed.")

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

with open(os.path.join(output_dir, "simulation_results.json")) as data_file:    
    data = json.load(data_file)

    
df_json = pd.json_normalize(data)

df_json = df_json.rename(columns={
    'adsorption_info.working_capacity_vacuum_swing': "working_capacity_vacuum_swing [mmol/g]",
    'adsorption_info.CO2_N2_selectivity': "CO2/N2_selectivity",
    'adsorption_info.CO2_uptake_P0.15bar_T298K': "CO2_uptake_P0.15bar_T298K [mmol/g]",
    'adsorption_info.CO2_uptake_P0.10bar_T363K': "CO2_uptake_P0.10bar_T363K [mmol/g]",
    'adsorption_info.CO2_heat_of_adsorption_P0.15bar_T298K': "heat_adsorption_CO2_P0.15bar_T298K [kcal/mol]",
    'adsorption_info.CO2_heat_of_adsorption_P0.10bar_T363K': "heat_adsorption_CO2_P0.10bar_T363K [kcal/mol]",
    'adsorption_info.N2_uptake_P0.85bar_T298K': "N2_binary_uptake_P0.85bar_T298K [mmol/g]",
    'adsorption_info.N2_heat_of_adsorption_P0.85bar_T298K': "heat_adsorption_N2_binary_P0.85bar_T298K [kcal/mol]",
    "uid": "CIF",
})

df_json = df_json.drop(columns=["info", "adsorption_info", "adsorption_info.file"])

df_json.to_csv(merged_results_path, index=False)
