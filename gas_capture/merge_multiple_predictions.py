import pandas as pd
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--model_name", default="", help="Name of the database in the resulting benchmark table.")
parser.add_argument("--csv_moftr_path", help="Path to the .csv file with properties predicted by MOFTransformer.", default=None)
parser.add_argument("--csv_sim_path", help="Path to the .csv file with properties predicted by MOFDiff simulation.", default=None)
parser.add_argument("--predictions_benchmark_path", help="Path to final .csv file", default="predictions_benchmark.csv")
args = parser.parse_args()

model_name = args.model_name
predictions_benchmark_path = args.predictions_benchmark_path

# Function to read CSV if path is provided
def read_csv_if_exists(path):
    return pd.read_csv(path) if path else None

# Read CSV files
csv_moftr = read_csv_if_exists(args.csv_moftr_path)
csv_sim = read_csv_if_exists(args.csv_sim_path)

# Determine which models are present
models = []
if csv_moftr is not None:
    models.append('MOFTransformer')
if csv_sim is not None:
    models.append('Simulation')

# Get all unique CIFs
all_cifs = pd.concat([df['CIF'] for df in [csv_moftr, csv_sim] if df is not None]).unique()

# Get all properties (excluding 'CIF' column)
all_properties = set()
for df in [csv_moftr, csv_sim]:
    if df is not None:
        all_properties.update([col for col in df.columns if col != 'CIF'])
all_properties = sorted(list(all_properties))

# Create multi-index columns
columns = pd.MultiIndex.from_product([all_properties, models])

# Create result dataframe
result_df = pd.DataFrame(index=all_cifs, columns=columns)

# Fill the result dataframe
for df, model in zip([csv_moftr, csv_sim], models):
    if df is not None:
        for prop in all_properties:
            if prop in df.columns:
                result_df.loc[df['CIF'], (prop, model)] = df.set_index('CIF')[prop]

# Drop subcolumns with all NaN values
columns_to_drop = []
for prop in all_properties:
    for model in models:
        if result_df[prop][model].isna().all():
            columns_to_drop.append((prop, model))

result_df = result_df.drop(columns=columns_to_drop)

# Reset index and rename the index column to 'CIF'
result_df = result_df.reset_index().rename(columns={'index': 'CIF'})

# Add model name to CIF if provided
if model_name != "":
    result_df['CIF'] = result_df['CIF'].apply(lambda x: f"{model_name}_{x}")

# Save the result
result_df.to_csv(predictions_benchmark_path, index=False)

print(f"Results saved to {predictions_benchmark_path}")
