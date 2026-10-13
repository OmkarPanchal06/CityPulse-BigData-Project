# CityPulse — GitHub Codespaces Big Data Project

**CityPulse: Big Data-Based Urban Pollution Intelligence System**

A reproducible, hardware-free educational simulation of an urban air-quality analytics pipeline. It uses synthetic observations, Hadoop Streaming MapReduce in Hadoop's **local execution mode**, Hive SQL with an embedded Derby metastore, Pandas validation, and Matplotlib charts. Run it in GitHub Codespaces; no local software or physical sensors are required.

> **Data and scope:** All generated values are synthetic and illustrative, not CPCB measurements, official AQI, or health advice. Hadoop runs as a single-node/local simulation, not a distributed multi-machine cluster. Hive executes real SQL against local files loaded into managed tables; it does not require HDFS daemons in this configuration.

## Repository layout

```text
.devcontainer/             Codespaces Dockerfile and configuration
.github/workflows/         Optional GitHub Actions execution
 data/                     Included sample CSV; generated CSV is created here
 scripts/generate_data.py  Deterministic synthetic data generator
 scripts/mapper.py         Hadoop Streaming mapper
 scripts/reducer.py        Hadoop Streaming reducer
 scripts/run_mapreduce.py  Hadoop local-mode job launcher
 scripts/validate_and_plot.py  Pandas cross-check and PNG charts
 scripts/run_hive.sh       Execute Hive SQL using embedded Derby
 scripts/run_all.sh        One-command complete pipeline
 sql/citypulse_queries.sql Hive DDL and analytical queries
 output/                   Generated outputs and logs (not committed by default)
 tests/                    Small mapper/reducer tests
```

## Start on GitHub (browser only)

1. Create a GitHub repository named `CityPulse-BigData-Project`.
2. Upload the **contents** of this project folder (not the outer ZIP folder) to the repository's `main` branch. Keep hidden folders `.devcontainer` and `.github`.
3. Open the repository on GitHub → **Code** → **Codespaces** → **Create codespace on main**.
4. The custom dev container builds Java 8, Hadoop 3.3.6, Hive 3.1.3 and the Python libraries. The first build downloads several large Apache packages and can take several minutes.
5. When the VS Code browser opens, open **Terminal → New Terminal** and wait for container setup to finish.
6. Run the environment check:

```bash
java -version
hadoop version
hive --version
python3 --version
```

7. Run the full project:

```bash
bash scripts/run_all.sh
```

The default is 10,000 synthetic records. To change the volume:

```bash
CITYPULSE_ROWS=50000 bash scripts/run_all.sh
```

## Run stages separately

```bash
python3 scripts/generate_data.py --rows 10000 --seed 42
python3 scripts/run_mapreduce.py
python3 scripts/validate_and_plot.py
bash scripts/run_hive.sh
```

## Expected outputs

- `data/citypulse_synthetic.csv` — generated synthetic source observations.
- `output/mapreduce/part-00000` — tab-separated city/month/pollutant mean and count from Hadoop Streaming.
- `output/monthly_pollution.csv` — structured MapReduce results.
- `output/city_pollutant_summary.csv` — city/pollutant summary.
- `output/monthly_pm25_by_city.png` — monthly PM2.5 trend chart.
- `output/city_pm25_ranking.png` — weighted city ranking chart.
- `output/hive/hive_execution.log` — Hive execution output and query results.

The validation step independently recomputes grouped means with Pandas and stops with an error if the MapReduce aggregates disagree. The terminal should report `VALIDATION PASSED` and the Hive log should contain the five query results.

## Hive details

`sql/citypulse_queries.sql` creates a database and two managed tables, loads the generated CSV and MapReduce TSV with `LOAD DATA LOCAL INPATH`, and runs five queries: monthly PM2.5 ranking, highest city per month, pollutant comparison, an explicitly illustrative threshold filter, and missing-value count. `scripts/run_hive.sh` substitutes the current absolute file paths before invoking Hive. Hive uses embedded Derby; it is not a separate metastore server.

## Tests

```bash
python3 -m pytest -q
```

## GitHub Actions (optional)

The workflow `.github/workflows/citypulse.yml` builds the same Docker environment and runs the full pipeline on pushes to `main` that touch project code, or manually from **Actions → CityPulse end-to-end simulation → Run workflow**. On completion, download the `citypulse-output` artifact from the run summary. The workflow is optional; Codespaces is the primary interactive environment.

## Troubleshooting

- **Container build fails downloading Apache archives:** retry the Codespace rebuild; if Apache archive hosting is temporarily unavailable, rebuild later. The image download is performed during the first container build.
- **`hadoop` or `hive` not found:** use **Codespaces: Rebuild Container** from the Command Palette (`Ctrl+Shift+P`) and wait for completion.
- **Output directory already exists:** the MapReduce launcher deletes only `output/mapreduce` before a new run; other outputs are refreshed by later stages.
- **Hive Derby lock:** do not run two Hive CLI sessions at the same time. Stop the previous Hive process and rerun `bash scripts/run_hive.sh`.
- **Codespaces quota:** stop the Codespace when finished using the Codespaces menu. Compute/storage allowances depend on your GitHub plan.

## Academic explanation

The mapper parses each observation, extracts the month, and emits three key-value pairs (one for each pollutant). Hadoop Streaming sorts mapper keys and passes grouped values to the reducer. The reducer computes arithmetic mean and record count per city/month/pollutant. Hive stores source and aggregate data in queryable tables and runs SQL analytics. Pandas independently verifies the MapReduce output; Matplotlib produces trend and ranking charts.

## Citation / provenance

The original sample CSV, notebook, mapper/reducer, and report were supplied in the project ZIP. The Codespaces and automation scaffolding is added in this repository. Apache Hadoop and Hive versions are pinned in `.devcontainer/Dockerfile` for reproducibility.
