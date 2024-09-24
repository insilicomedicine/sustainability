import moftransformer
from moftransformer.utils import prepare_data
from moftransformer import predict
import os
import json
import argparse
from pathlib import Path
import shutil
import sys
import re

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cif_input_path", help="Path to the directory with input .cif files.", required=True)
    parser.add_argument("--models_dir", help="Path to the models", default="models")
    parser.add_argument("--output_folder", help="Path to the directory to save output", default="output_predictions")
    parser.add_argument("--preprocessed_cifs_dir", help="Path to save preprocessed cifs", default="preprocessed_cifs")
    return parser.parse_args()

def clean_property_name(prop_name):
    # Remove dataset prefix and training info postfix
    prop_name = re.sub(r'^(ARC-MOF|MOFXDB|BW-DB)_', '', prop_name)
    prop_name = re.sub(r'_\d+epochs.*$', '', prop_name)
    return prop_name

def get_model_info(model_dir):
    if model_dir.startswith(("logs_20k_", "logs_full_")):
        prefix = "logs_20k_" if model_dir.startswith("logs_20k_") else "logs_full_"
        prop_name = model_dir[len(prefix):]
        clean_prop = clean_property_name(prop_name)
        use_custom_normalization = "mean0_std1" in model_dir
        return prefix, clean_prop, use_custom_normalization
    return None, None, False

def prepare_dummy_values(cif_files_dir, properties_list):
    cif_files = [f for f in os.listdir(cif_files_dir) if f.endswith(".cif")]
    dummy_values = {cif.split(".cif")[0]: 0.0 for cif in cif_files}
    
    for prop in properties_list:
        with open(os.path.join(cif_files_dir, f"raw_{prop}.json"), "w") as f:
            json.dump(dummy_values, f)

def get_checkpoint_path(model_dir):
    checkpoint_dir = os.path.join(model_dir, "pretrained_mof_seed0_from_pmtransformer/version_0/checkpoints")
    best_ckpt = os.path.join(checkpoint_dir, "best.ckpt")
    last_ckpt = os.path.join(checkpoint_dir, "last.ckpt")
    
    if os.path.exists(best_ckpt):
        return best_ckpt
    elif os.path.exists(last_ckpt):
        print(f"Warning: 'best.ckpt' not found in {checkpoint_dir}. Using 'last.ckpt' instead.")
        return last_ckpt
    else:
        raise FileNotFoundError(f"No checkpoint file found in {checkpoint_dir}")

def run_predictions(args, models_list, properties_list):
    for model_dir in models_list:
        prefix, prop, use_custom_normalization = get_model_info(model_dir)
        
        if prop is None:  # Skip if not a valid model directory
            continue

        if model_dir == "bandgap_and_h2_uptake":
            for additional_prop in ["bandgap", "h2_uptake"]:
                predict(
                    mean=0, std=1,
                    root_dataset=args.preprocessed_cifs_dir,
                    load_path=os.path.join(args.models_dir, "bandgap_and_h2_uptake", f"finetuned_{additional_prop}.ckpt"),
                    downstream=additional_prop,
                    split="test",
                    save_dir=os.path.join(args.output_folder, additional_prop),
                )
        else:
            try:
                checkpoint_path = get_checkpoint_path(os.path.join(args.models_dir, model_dir))
                predict_kwargs = {
                    "root_dataset": args.preprocessed_cifs_dir,
                    "load_path": checkpoint_path,
                    "downstream": prop,
                    "split": "test",
                    "save_dir": os.path.join(args.output_folder, prop),
                }
                
                if use_custom_normalization:
                    predict_kwargs.update({"mean": 0, "std": 1})
                
                predict(**predict_kwargs)
            except FileNotFoundError as e:
                print(f"Error: {e}")
                print(f"Skipping prediction for {prop}")

def cleanup(args):
    json_files_input_dir = [f for f in os.listdir(args.cif_input_path) if f.endswith(".json")]
    for json_file in json_files_input_dir:
        os.remove(os.path.join(args.cif_input_path, json_file))

    shutil.rmtree(args.preprocessed_cifs_dir, ignore_errors=True)
    shutil.rmtree("logs/", ignore_errors=True)

def main():
    args = parse_arguments()
    cif_files_dir = Path(args.cif_input_path)

    if not cif_files_dir.exists():
        print("The provided directory doesn't exist.")
        raise SystemExit(1)

    if os.path.exists(args.output_folder) and os.listdir(args.output_folder):
        response = input(f"The directory '{args.output_folder}' is not empty. Do you want to delete its contents? (y/n): ").lower()
        
        if response == 'y':
            try:
                shutil.rmtree(args.output_folder)
                os.makedirs(args.output_folder)
                print(f"Directory '{args.output_folder}' has been cleared.")
            except Exception as e:
                print(f"An error occurred while clearing the directory: {e}")
                sys.exit(1)
        else:
            print("Operation cancelled. Exiting the script.")
            sys.exit(0)
    else:
        print(f"The directory '{args.output_folder}' is empty or doesn't exist. Proceeding with the script.")

    models_list = [m for m in os.listdir(args.models_dir) if os.path.isdir(os.path.join(args.models_dir, m))]
    properties_list = [clean_property_name(get_model_info(m)[1]) for m in models_list if get_model_info(m)[1] is not None]
    properties_list.extend(["bandgap", "h2_uptake"])

    prepare_dummy_values(cif_files_dir, properties_list)
    
    prepare_data(cif_files_dir, args.preprocessed_cifs_dir, downstream=properties_list, test_fraction=1.0, train_fraction=0.0) 

    run_predictions(args, models_list, properties_list)
    
    cleanup(args)

if __name__ == "__main__":
    main()