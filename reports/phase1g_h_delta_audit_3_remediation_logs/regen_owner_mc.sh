#!/bin/bash
cd /home/user/timescape-fsigma8
R4="${SCRATCH:?set SCRATCH to a scratch directory outside the repository}"
export OPENBLAS_NUM_THREADS=1 PYTHONPATH=src
t0=$(date +%s)
.venv/bin/python -B scripts/phase1g_owner_decisions_numerics.py > $R4/regen_owner_decisions.log 2>&1
echo "phase1g_owner_decisions_numerics rc=$? seconds=$(( $(date +%s) - t0 ))"
