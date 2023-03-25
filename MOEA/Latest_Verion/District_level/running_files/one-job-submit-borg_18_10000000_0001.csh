#!/bin/tcsh

# Set up conda

conda activate /usr/local/usrapps/infews/group_env

# Submit LSF job

bsub -n 8 -q shared_memory -R "span[hosts=1]" -R "rusage[mem=5GB]" -W 10000 -o out.%J -e err.%J "python 1-platypus_BETO_district_multiyear_borg_energy_GHG_18_10000000_0001.py"

conda deactivate

	
