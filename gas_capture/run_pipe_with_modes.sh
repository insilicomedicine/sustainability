#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 /path/to/input_cifs database_name [mofdiff|moftransformer|both] outputpath"
    exit 1
fi

INPUT_PATH="$1"
MODEL_NAME="$2"
PREDICTION_TYPE="$3"
OUTPUT="$4"

# Ensure the input path is absolute
if [[ ! "$INPUT_PATH" = /* ]]; then
    INPUT_PATH="$PWD/$INPUT_PATH"
fi

echo "Starting MOF property prediction and benchmarking pipeline..."

# Function to check if results already exist
check_results() {
    local csv_file="$1"
    if [ -f "$csv_file" ] && [ $(wc -l < "$csv_file") -gt 1 ]; then
        return 0  # Results exist
    else
        return 1  # Results don't exist or file is empty
    fi
}

# Function to run MOFDiff simulation
run_mofdiff() {
    echo "Checking MOFDiff results..."
    MOFDIFF_CSV="$PWD/MOFDiff_simulation/mof_diff_merged_results_$MODEL_NAME.csv"
    if check_results "$MOFDIFF_CSV"; then
        echo "MOFDiff results already exist. Skipping simulation."
    else
        echo "Running MOFDiff simulation..."
        cd MOFDiff_simulation
        docker run -v "$INPUT_PATH":/v/cif_input raspa2_sim_build
        python gather_results.py --cif_input_path "$INPUT_PATH" --merged_results_path="mof_diff_merged_results_$MODEL_NAME.csv"
        cd ..
    fi
}

# Function to run MOFTransformer prediction
run_moftransformer() {
    echo "Checking MOFTransformer results..."
    MOFTRANSFORMER_CSV="$PWD/MOFTransformer_prediction/mof_transformer_merged_results_$MODEL_NAME.csv"
    if check_results "$MOFTRANSFORMER_CSV"; then
        echo "MOFTransformer results already exist. Skipping prediction."
    else
        echo "Running MOFTransformer prediction..."
        cd MOFTransformer_prediction
        python predict.py --cif_input_path "$INPUT_PATH" --output_folder "output_predictions_$MODEL_NAME" --preprocessed_cifs_dir "preprocessed_cifs_$MODEL_NAME"
        python gather_results.py --merged_results_path="mof_transformer_merged_results_$MODEL_NAME.csv" --output_dir "output_predictions_$MODEL_NAME"
        cd ..
    fi
}

# Run the selected prediction type(s)
case $PREDICTION_TYPE in
    mofdiff)
        run_mofdiff
        python merge_multiple_predictions.py --model_name "$MODEL_NAME" --csv_sim_path "$MOFDIFF_CSV" --predictions_benchmark_path "$OUTPUT"
        ;;
    moftransformer)
        run_moftransformer
        python merge_multiple_predictions.py --model_name "$MODEL_NAME" --csv_moftr_path "$MOFTRANSFORMER_CSV" --predictions_benchmark_path "$OUTPUT"
        ;;
    both)
        run_mofdiff
        run_moftransformer
        python merge_multiple_predictions.py --model_name "$MODEL_NAME" --csv_moftr_path "$MOFTRANSFORMER_CSV" --csv_sim_path "$MOFDIFF_CSV" --predictions_benchmark_path "$OUTPUT"
        ;;
    *)
        echo "Invalid prediction type. Please choose 'mofdiff', 'moftransformer', or 'both'."
        exit 1
        ;;
esac

echo "Pipeline completed. Results saved in $OUTPUT"