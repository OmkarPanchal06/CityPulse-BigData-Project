#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/generate_data.py --rows "${CITYPULSE_ROWS:-10000}" --seed 42
python3 scripts/run_mapreduce.py
python3 scripts/validate_and_plot.py
bash scripts/run_hive.sh
printf '\nALL STEPS COMPLETED. See output/ and output/hive/hive_execution.log\n'
