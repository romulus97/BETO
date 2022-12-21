#!/bin/tcsh

# Set up conda

conda activate /usr/local/usrapps/infews/group_env

# Submit LSF job

bsub -n 16 -q shared_memory -R "span[hosts=1]" -R "rusage[mem=60GB]" -W 10000 -x -o out.%J -e err.%J "python platypus_BETO_district_multiyear_borg_energy_GHG.py"

conda deactivate

	
