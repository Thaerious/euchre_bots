#!/bin/bash
#SBATCH --account=def-edward
#SBATCH --ntasks=16              # number of MPI processes
#SBATCH --mem-per-cpu=1024M      # memory; default unit is megabytes
#SBATCH --time=0-01:00           # time (DD-HH:MM)

echo submit_mpi.sh
mpirun -np 16 python examples/mpi.py -c 10