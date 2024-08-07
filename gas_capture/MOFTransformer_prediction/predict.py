import moftransformer
from moftransformer.utils import prepare_data
from moftransformer import predict
import os
import json
import argparse
from pathlib import Path
import shutil
import sys


parser = argparse.ArgumentParser()
parser.add_argument("--cif_input_path", help="Path to the directory with input .cif files.", required=True)
parser.add_argument("--models_dir", help="Path to the models", default="models")
parser.add_argument("--output_folder", help="Path to the directory to save output", default="output_predictions")
parser.add_argument("--preprocessed_cifs_dir", help="Path to save preprocessed cifs", default="preprocessed_cifs")
args = parser.parse_args()
cif_files_dir = Path(args.cif_input_path)
output_dir = args.output_folder
models_dir = args.models_dir
preprocessed_cifs_dir = args.preprocessed_cifs_dir

if not cif_files_dir.exists():
    print("The provided directory doesn't exist.")
    raise SystemExit(1)

### TODO: maybe change it
model_dir_prefix = "logs_20k_"

if os.path.exists(output_dir) and os.listdir(output_dir):
    response = input(f"The directory '{output_dir}' is not empty. Do you want to delete its contents? (y/n): ").lower()
    
    if response == 'y':
        try:
            shutil.rmtree(output_dir)
            os.makedirs(output_dir)
            print(f"Directory '{output_dir}' has been cleared.")
        except Exception as e:
            print(f"An error occurred while clearing the directory: {e}")
            sys.exit(1)
    else:
        print("Operation cancelled. Exiting the script.")
        sys.exit(0)
else:
    print(f"The directory '{output_dir}' is empty or doesn't exist. Proceeding with the script.")

models_list = [m for m in os.listdir(models_dir) if m.startswith(model_dir_prefix) and os.path.isdir(os.path.join(models_dir, m))]
properties_list = [m.split(model_dir_prefix)[1] for m in models_list if m.startswith(model_dir_prefix)]
cif_files = [f for f in os.listdir(cif_files_dir) if f.endswith(".cif")]

dummy_values = {cif.split(".cif")[0]:0.0 for cif in cif_files}

for prop in properties_list:
    with open(os.path.join(cif_files_dir, f"raw_{prop}.json"), "w") as f:
        json.dump(dummy_values, f)
        
prepare_data(cif_files_dir, preprocessed_cifs_dir, downstream=properties_list, test_fraction=1.0, train_fraction=0.0) 

for prop in properties_list:
    predict(
        # accelerator='cpu',
        # devices=8,
        root_dataset=preprocessed_cifs_dir,
        load_path=os.path.join(models_dir, model_dir_prefix + prop, "pretrained_mof_seed0_from_pmtransformer/version_0/checkpoints/best.ckpt"),
        downstream=prop,
        split="test",  # or "all" if you want to predict on all data
        save_dir=os.path.join(output_dir, prop),
    )
    
# Cleaning up intermediary files and dirs
json_files_input_dir = [f for f in os.listdir(cif_files_dir) if f.endswith(".json")]
for json_file in json_files_input_dir:
    os.remove(os.path.join(cif_files_dir, json_file))

shutil.rmtree(preprocessed_cifs_dir, ignore_errors=True)
shutil.rmtree("logs/", ignore_errors=True)
