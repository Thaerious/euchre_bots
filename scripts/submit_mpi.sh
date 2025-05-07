#!/bin/bash
#SBATCH --account=def-edward
#SBATCH --ntasks=1               # number of MPI processes
#SBATCH --mem-per-cpu=1024M      # memory; default unit is megabytes
#SBATCH --time=1-00:00           # time (DD-HH:MM)
srun python ../examples/mpi.py -c 10 &