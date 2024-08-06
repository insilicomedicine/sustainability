#!/bin/bash

if [ $(find /v/cif_input -maxdepth 1 -name "*.cif" | wc -l) -eq 0 ]; then
    echo "Error: No .cif files found in the provided input folder"
    exit 1
fi

mkdir /root/MOFDiff_simulate
cd /root/MOFDiff_simulate
cp -r /v/cif_input/ .
mv cif_input/ relaxed/

echo "[$(find $(pwd)/relaxed -maxdepth 1 -name '*.cif' | sed 's/^/"/;s/$/"/' | tr '\n' ',' | sed 's/,$//')]" > valid_mof_paths.json
cat valid_mof_paths.json
cd /root/MOFDiff

python mofdiff/scripts/calculate_charges.py --input /root/MOFDiff_simulate

python mofdiff/scripts/gcmc_screen.py --input /root/MOFDiff_simulate/mepo_qeq_charges --rewrite_raspa_input

cp -r /root/MOFDiff_simulate/mepo_qeq_charges/gcmc/screening_results.json /v/cif_input/simulation_results.json
chmod -R 777 /v/cif_input/