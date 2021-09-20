#!/bin/tcsh

# Set up conda

conda activate /usr/local/usrapps/infews/group_env

# Submit LSF job

bsub -n 8 -R "span[hosts=1]" -R "rusage[mem=30GB]" -W 5000 -x -o out.%J -e err.%J "python platypus_BETO_V_district_multiyear_borg.py"

conda deactivate

	
