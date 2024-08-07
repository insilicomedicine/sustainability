# MOF Property Prediction and Benchmarking

This project combines the MOFDiff simulation and MOFTransformer prediction tools to evaluate and benchmark Metal-Organic Frameworks (MOFs) properties.

## Prerequisites

- Docker
- Python 3.10 (recommended)
- CUDA-compatible GPU (optional, but recommended for faster predictions)

## Setup

1. Clone this repository and navigate to the project root.

2. Ensure you have a folder containing only the `.cif` files you want to evaluate.

3. Install the required Python packages:

```bash
cd MOFTransformer_prediction/
pip install -r requirements.txt
```

4. Pull the Docker image for MOFDiff simulation:
```bash
docker pull akhmedins/benchmark_raspa2_sim:latest
```

5. Download and extract the model checkpoints for MOFTransformer:
```bash
wget https://zenodo.org/records/13197825/files/models.tar.gz
tar -zxvf models.tar.gz
```

## Usage

1. Place your .cif files in a folder (e.g., input_cifs/).

2. Run the end-to-end pipeline:
```bash
cd ..
./run_pipeline_with_modes.sh /path/to/input_cifs model_name [mofdiff|moftransformer|both] output_file_name.csv
```
Where:

* /path/to/input_cifs is the absolute path to your input folder containing .cif files
* model_name is the desired name for your model in the resulting benchmark table
* [mofdiff|moftransformer|both] specifies which prediction method to use:
  * mofdiff: Run only MOFDiff simulation
  * moftransformer: Run only MOFTransformer prediction
  * both: Run both MOFDiff and MOFTransformer

* output_file_name.csv is the name of the output file where results will be saved

Replace /path/to/input_cifs with the absolute path to your input folder and model_name with the desired name for your database in the resulting benchmark table.


## Output

The output CSV file (specified as the last argument in the command) will contain the following properties for each MOF:
- Working capacity under vacuum swing conditions (mmol/g)
- Selectivity of CO₂ over N₂
- CO₂ uptake at 0.15 bar and 298 K (mmol/g)
- CO₂ uptake at 0.10 bar and 363 K (mmol/g)
- Heat of adsorption for CO₂ at 0.15 bar and 298 K (kcal/mol)
- Heat of adsorption for CO₂ at 0.10 bar and 363 K (kcal/mol)
- N₂ uptake in binary mixture at 0.85 bar and 298 K (mmol/g)
- Heat of adsorption for N₂ in binary mixture at 0.85 bar and 298 K (kcal/mol)

The table will include predictions from both MOFDiff simulation and MOFTransformer.

## Example Benchmark Table

<div>
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th>CIF</th>
      <th colspan="2" halign="left">heat_adsorption_CO2_P0.15bar_T298K [kcal/mol]</th>
      <th colspan="2" halign="left">heat_adsorption_CO2_P0.10bar_T363K [kcal/mol]</th>
      <th colspan="2" halign="left">CO2/N2_selectivity</th>
      <th colspan="2" halign="left">N2_binary_uptake_P0.85bar_T298K [mmol/g]</th>
      <th colspan="2" halign="left">CO2_uptake_P0.15bar_T298K [mmol/g]</th>
      <th colspan="2" halign="left">working_capacity_vacuum_swing [mmol/g]</th>
      <th colspan="2" halign="left">heat_adsorption_N2_binary_P0.85bar_T298K [kcal/mol]</th>
      <th colspan="2" halign="left">CO2_uptake_P0.10bar_T363K [mmol/g]</th>
    </tr>
    <tr>
      <th></th>
      <th>MOFTransformer</th>
      <th>Simulation</th>
      <th>MOFTransformer</th>
      <th>Simulation</th>
      <th>MOFTransformer</th>
      <th>Simulation</th>
      <th>MOFTransformer</th>
      <th>Simulation</th>
      <th>MOFTransformer</th>
      <th>Simulation</th>
      <th>MOFTransformer</th>
      <th>Simulation</th>
      <th>MOFTransformer</th>
      <th>Simulation</th>
      <th>MOFTransformer</th>
      <th>Simulation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>ExampleDB_sample_20</th>
      <td>4.992188</td>
      <td>4.491592</td>
      <td>4.632812</td>
      <td>4.333871</td>
      <td>7.796875</td>
      <td>1.127828</td>
      <td>0.175781</td>
      <td>0.163640</td>
      <td>0.403076</td>
      <td>0.184558</td>
      <td>0.256348</td>
      <td>0.150945</td>
      <td>2.847656</td>
      <td>2.627568</td>
      <td>0.059082</td>
      <td>0.033613</td>
    </tr>
    <tr>
      <th>ExampleDB_sample_21</th>
      <td>5.371094</td>
      <td>5.455796</td>
      <td>4.480469</td>
      <td>5.359613</td>
      <td>15.796875</td>
      <td>3.385736</td>
      <td>0.183716</td>
      <td>0.160205</td>
      <td>0.536133</td>
      <td>0.542413</td>
      <td>0.443604</td>
      <td>0.478580</td>
      <td>2.634766</td>
      <td>2.650780</td>
      <td>0.101013</td>
      <td>0.063832</td>
    </tr>
    <tr>
      <th>ExampleDB_sample_23</th>
      <td>6.054688</td>
      <td>34.916194</td>
      <td>6.410156</td>
      <td>-335.459877</td>
      <td>16.437500</td>
      <td>6.034865</td>
      <td>0.149414</td>
      <td>0.204346</td>
      <td>0.961914</td>
      <td>1.233199</td>
      <td>0.686523</td>
      <td>0.503254</td>
      <td>3.498047</td>
      <td>-138.778409</td>
      <td>0.094116</td>
      <td>0.729945</td>
    </tr>
    <tr>
      <th>ExampleDB_sample_24</th>
      <td>4.652344</td>
      <td>4.800805</td>
      <td>4.144531</td>
      <td>4.247083</td>
      <td>7.289062</td>
      <td>1.262893</td>
      <td>0.196655</td>
      <td>0.235443</td>
      <td>0.354492</td>
      <td>0.297339</td>
      <td>0.230469</td>
      <td>0.251543</td>
      <td>2.427734</td>
      <td>2.477118</td>
      <td>0.085510</td>
      <td>0.045797</td>
    </tr>
    <tr>
      <th>ExampleDB_sample_25</th>
      <td>4.113281</td>
      <td>4.053065</td>
      <td>3.855469</td>
      <td>3.755058</td>
      <td>6.062500</td>
      <td>0.898120</td>
      <td>0.228638</td>
      <td>0.180196</td>
      <td>0.276855</td>
      <td>0.161838</td>
      <td>0.199097</td>
      <td>0.124192</td>
      <td>2.365234</td>
      <td>2.006219</td>
      <td>0.085876</td>
      <td>0.037646</td>
    </tr>
    <tr>
      <th>ExampleDB_sample_26</th>
      <td>5.234375</td>
      <td>NaN</td>
      <td>4.925781</td>
      <td>NaN</td>
      <td>10.835938</td>
      <td>NaN</td>
      <td>0.293457</td>
      <td>NaN</td>
      <td>0.882812</td>
      <td>NaN</td>
      <td>0.770508</td>
      <td>NaN</td>
      <td>2.812500</td>
      <td>NaN</td>
      <td>0.195435</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>ExampleDB_sample_27</th>
      <td>4.011719</td>
      <td>4.005387</td>
      <td>3.816406</td>
      <td>3.533202</td>
      <td>5.886719</td>
      <td>0.923698</td>
      <td>0.250244</td>
      <td>0.232439</td>
      <td>0.283691</td>
      <td>0.214704</td>
      <td>0.203125</td>
      <td>0.171601</td>
      <td>2.080078</td>
      <td>2.042183</td>
      <td>0.090820</td>
      <td>0.043103</td>
    </tr>
    <tr>
      <th>ExampleDB_sample_28</th>
      <td>5.566406</td>
      <td>6.381018</td>
      <td>5.089844</td>
      <td>5.976778</td>
      <td>17.171875</td>
      <td>4.763436</td>
      <td>0.187866</td>
      <td>0.171973</td>
      <td>0.528320</td>
      <td>0.819184</td>
      <td>0.427979</td>
      <td>0.726423</td>
      <td>2.962891</td>
      <td>3.222045</td>
      <td>0.073303</td>
      <td>0.092761</td>
    </tr>
    <tr>
      <th>ExampleDB_sample_29</th>
      <td>3.480469</td>
      <td>3.455531</td>
      <td>3.101562</td>
      <td>2.911063</td>
      <td>4.816406</td>
      <td>0.678424</td>
      <td>0.178955</td>
      <td>0.161567</td>
      <td>0.174194</td>
      <td>0.109611</td>
      <td>0.101318</td>
      <td>0.080514</td>
      <td>1.826172</td>
      <td>1.672587</td>
      <td>0.058533</td>
      <td>0.029097</td>
    </tr>
  </tbody>
</table>
</div>

## Benchmark Table

The below table shows the evaluation of 8 sets of generated MOFs by the MOFDiff model. Generations targeted each of the 8 evaluated properties, with the target set to `15.0`.

[BENCHMARK_TABLE](benchmark.csv)


## Troubleshooting
If you encounter any issues, please check the individual README files in the MOFDiff_simulation/ and MOFTransformer_prediction/ directories for more detailed instructions and troubleshooting tips.