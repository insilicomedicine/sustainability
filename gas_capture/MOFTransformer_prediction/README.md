# MOFTransformer Gas Absorption Properties Prediction

This guide outlines the procedure for predicting gas absorption properties of metal-organic frameworks (MOFs) using the [MOFTransformer](https://github.com/hspark1212/MOFTransformer) model.

## Prerequisites

- Python 3.10 (recommended)
- CUDA-compatible GPU (optional, but highly recommended for faster predictions)

## Installation

1. Create and activate a new Python environment (optional but recommended).

2. Upgrade pip and install the required packages:

   ```bash
   pip install pip==24.0
   pip install -r requirements.txt
   ```

   > **Note**: The pip downgrade is necessary to support an outdated package in `requirements.txt`.

3. Ensure PyTorch is compatible with your CUDA/driver version:

   If the automatically installed PyTorch version is incompatible, reinstall the correct version by following the [official PyTorch guidelines](https://pytorch.org/get-started/locally/).

4. Download and extract the model checkpoints:

   ```bash
   wget https://zenodo.org/records/13815098/files/models.tar.gz
   tar -zxvf models.tar.gz
   ```

## Usage

1. Predict properties for MOF structures:

   ```bash
   python predict.py --cif_input_path <path_to_input_folder>
   ```

   Replace `<path_to_input_folder>` with the absolute or relative path to the folder containing your `.cif` files.

   > **Note**: The script uses the first available GPU. For CPU-only systems, uncomment and increase the `devices` argument in the `predict()` function for multiprocessing. Be aware that CPU predictions are significantly slower.

2. Gather and format the results:

   ```bash
   python gather_results.py
   ```

   This script combines the individual prediction results into a single CSV file.

## Output

The final results are stored in `merged_results.csv`. Each row represents a MOF structure, and columns represent different predicted properties.

### Output Format

| Column Name | Description | Unit |
|-------------|-------------|------|
| CIF | Name of the input CIF file | - |
| heat_adsorption_CO2_P0.15bar_T298K | Heat of adsorption for CO₂ at 0.15 bar and 298 K | kcal/mol |
| heat_adsorption_CO2_P0.10bar_T363K | Heat of adsorption for CO₂ at 0.10 bar and 363 K | kcal/mol |
| CO2/N2_selectivity | CO₂/N₂ selectivity | - |
| N2_binary_uptake_P0.85bar_T298K | N₂ uptake in binary mixture at 0.85 bar and 298 K | mmol/g |
| CO2_uptake_P0.15bar_T298K | CO₂ uptake at 0.15 bar and 298 K | mmol/g |
| working_capacity_vacuum_swing | Working capacity under vacuum swing conditions | mmol/g |
| heat_adsorption_N2_binary_P0.85bar_T298K | Heat of adsorption for N₂ in binary mixture at 0.85 bar and 298 K | kcal/mol |
| CO2_uptake_P0.10bar_T363K | CO₂ uptake at 0.10 bar and 363 K | mmol/g |

### Sample Output

| CIF | heat_adsorption_CO2_P0.15bar_T298K [kcal/mol] | heat_adsorption_CO2_P0.10bar_T363K [kcal/mol] | CO2/N2_selectivity | N2_binary_uptake_P0.85bar_T298K [mmol/g] | CO2_uptake_P0.15bar_T298K [mmol/g] | working_capacity_vacuum_swing [mmol/g] | heat_adsorption_N2_binary_P0.85bar_T298K [kcal/mol] | CO2_uptake_P0.10bar_T363K [mmol/g] |
|-----|------------------------------------------------|------------------------------------------------|--------------------|-------------------------------------------|------------------------------------|-----------------------------------------|-----------------------------------------------------|-------------------------------------|
| sample_20 | 4.9921875 | 4.6328125 | 7.796875 | 0.17578125 | 0.403076171875 | 0.25634765625 | 2.84765625 | 0.05908203125 |
| sample_21 | 5.37109375 | 4.48046875 | 15.796875 | 0.1837158203125 | 0.5361328125 | 0.443603515625 | 2.634765625 | 0.10101318359375 |
| sample_23 | 6.0546875 | 6.41015625 | 16.4375 | 0.1494140625 | 0.9619140625 | 0.6865234375 | 3.498046875 | 0.0941162109375 |
| sample_24 | 4.65234375 | 4.14453125 | 7.2890625 | 0.1966552734375 | 0.3544921875 | 0.23046875 | 2.427734375 | 0.08551025390625 |
| sample_25 | 4.11328125 | 3.85546875 | 6.0625 | 0.2286376953125 | 0.27685546875 | 0.1990966796875 | 2.365234375 | 0.08587646484375 |
| sample_26 | 5.234375 | 4.92578125 | 10.8359375 | 0.29345703125 | 0.8828125 | 0.7705078125 | 2.8125 | 0.1954345703125 |
| sample_27 | 4.01171875 | 3.81640625 | 5.88671875 | 0.250244140625 | 0.28369140625 | 0.203125 | 2.080078125 | 0.0908203125 |
| sample_28 | 5.56640625 | 5.08984375 | 17.171875 | 0.1878662109375 | 0.5283203125 | 0.427978515625 | 2.962890625 | 0.07330322265625 |
| sample_29 | 3.48046875 | 3.1015625 | 4.81640625 | 0.178955078125 | 0.1741943359375 | 0.101318359375 | 1.826171875 | 0.05853271484375 |

## Additional Information

- Intermediate prediction results are stored in the `output_predictions/` folder, organized by property.
- For more details about the MOFTransformer model, visit the [original repository](https://github.com/hspark1212/MOFTransformer).