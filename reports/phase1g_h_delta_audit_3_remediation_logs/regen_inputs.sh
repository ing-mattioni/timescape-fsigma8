#!/bin/bash
# Regenerate the git-ignored inputs whose absence skips 32 tests (no source edits).
cd /home/user/timescape-fsigma8
R4="${SCRATCH:?set SCRATCH to a scratch directory outside the repository}"
export OPENBLAS_NUM_THREADS=1 PYTHONPATH=src
for s in execute_upstream_notebook extract_upstream_oracle extract_upstream_perturbation_oracle \
         extract_upstream_barotropic_oracle validate_growth_pipeline validate_barotropic_perturbations; do
  t0=$(date +%s)
  .venv/bin/python -B scripts/$s.py > $R4/regen_$s.log 2>&1
  echo "$s rc=$? seconds=$(( $(date +%s) - t0 ))"
done
