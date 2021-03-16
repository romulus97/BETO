#!/bin/tcsh

# Set up python
conda activate /usr/local/usrapps/infews/CAPOW_env

bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python platypus_BETO_C.py"

conda deactivate

	
