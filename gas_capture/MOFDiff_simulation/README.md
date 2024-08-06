# MOFDiff Simulation

This guide outlines the procedure for obtaining gas absorption properties of metal-organic frameworks (MOFs) using the simulation approach adopted from [MOFDiff](https://github.com/microsoft/MOFDiff). The simulation utilizes RASPA2 and eGULP tools.

## Prerequisites

We provide a pre-built Docker image for Linux-x86 systems with all necessary tools pre-installed.

## Setup

1. Pull the Docker image:

   ```bash
   docker pull akhmedins/benchmark_raspa2_sim:latest
   ```

2. Build the simulation container (execute in the directory containing the Dockerfile):

   ```bash
   docker build -t raspa2_sim_build .
   ```

## Running the Simulation

Run the simulation by providing the **absolute path** (or a relative path containing `$PWD`) to an input folder containing `.cif` files:

```bash
docker run -v $PWD/cif_sample_input:/v/cif_input raspa2_sim_build
```

> **Note**: Replace `$PWD/cif_sample_input` with the actual path to your input folder.

> **Warning**: Simulation duration can range from 10 minutes to several hours, depending on the number of input `.cif` files and CPU capabilities.

## Results

The simulation results are stored in a `simulation_results.json` file within the provided input folder. Each entry in the JSON file represents a simulated MOF and its properties.

To reformat the results into a CSV file, run:

```bash
python gather_results.py --cif_input_path <path_to_input_folder>
```
Replace `<path_to_input_folder>` with the absolute or relative path to the folder containing your `.cif` files and the newly generated `simulation_results.json` file.

The final results will be stored in the `merged_results.csv` file.

### Output Format

The `merged_results.csv` file contains the following columns:

| Column Name | Description | Unit |
|-------------|-------------|------|
| CIF | Name of the input CIF file | - |
| heat_adsorption_CO2_P0.15bar_T298K | Heat of adsorption for CO₂ at 0.15 bar and 298 K | kcal/mol |
| heat_adsorption_CO2_P0.10bar_T363K | Heat of adsorption for CO₂ at 0.10 bar and 363 K | kcal/mol |
| CO2/N2_selectivity | CO₂/N₂ selectivity | - |
| N2_binary_uptake_P0.85bar_T298K | N₂ uptake at 0.85 bar and 298 K | mmol/g |
| CO2_uptake_P0.15bar_T298K | CO₂ uptake at 0.15 bar and 298 K | mmol/g |
| working_capacity_vacuum_swing | Working capacity under vacuum swing conditions | mmol/g |
| heat_adsorption_N2_binary_P0.85bar_T298K | Heat of adsorption for N₂ at 0.85 bar and 298 K | kcal/mol |
| CO2_uptake_P0.10bar_T363K | CO₂ uptake at 0.10 bar and 363 K | mmol/g |

Sample output:

| CIF | heat_adsorption_CO2_P0.15bar_T298K [kcal/mol] | heat_adsorption_CO2_P0.10bar_T363K [kcal/mol] | CO2/N2_selectivity | N2_binary_uptake_P0.85bar_T298K [mmol/g] | CO2_uptake_P0.15bar_T298K [mmol/g] | working_capacity_vacuum_swing [mmol/g] | heat_adsorption_N2_binary_P0.85bar_T298K [kcal/mol] | CO2_uptake_P0.10bar_T363K [mmol/g] |
|-----|------------------------------------------------|------------------------------------------------|--------------------|-------------------------------------------|------------------------------------|-----------------------------------------|-----------------------------------------------------|-------------------------------------|
| sample_20 | 4.9921875 | 4.6328125 | 7.796875 | 0.17578125 | 0.403076171875 | 0.25634765625 | 2.84765625 | 0.05908203125 |
| sample_21 | 5.37109375 | 4.48046875 | 15.796875 | 0.1837158203125 | 0.5361328125 | 0.443603515625 | 2.634765625 | 0.10101318359375 |

> **Note**: All uptake values are in mmol/g, and heat of adsorption values are in kcal/mol.