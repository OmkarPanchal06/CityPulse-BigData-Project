#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
command -v hive >/dev/null || { echo 'Hive CLI not found. Rebuild the Codespace container.'; exit 1; }
mkdir -p "$ROOT/output/hive"
if [ ! -d /opt/hive-metastore/metastore_db ]; then
  schematool -dbType derby -initSchema
fi
# Create a portable SQL file by replacing the input/output path placeholders.
sed \
  -e "s|__RAW_CSV_PATH__|$ROOT/data/citypulse_synthetic.csv|g" \
  -e "s|__MR_OUTPUT_PATH__|$ROOT/output/mapreduce/part-00000|g" \
  "$ROOT/sql/citypulse_queries.sql" > "$ROOT/output/hive/run_queries.sql"
# Embedded Derby metastore and local MapReduce execution: no HDFS daemon needed.
hive --hiveconf hive.execution.engine=mr \
     --hiveconf mapreduce.framework.name=local \
     --hiveconf fs.defaultFS=file:/// \
     --hiveconf hive.exec.mode.local.auto=true \
     -f "$ROOT/output/hive/run_queries.sql" \
     2>&1 | tee "$ROOT/output/hive/hive_execution.log"
echo "Hive execution log: $ROOT/output/hive/hive_execution.log"
