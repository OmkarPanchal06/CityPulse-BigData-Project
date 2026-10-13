# CityPulse: Big Data-Based Urban Pollution Intelligence System

## Abstract
CityPulse is an educational Big Data simulation that aggregates urban air-pollution readings by city, month, and pollutant. It demonstrates synthetic data generation, Hadoop Streaming MapReduce, Hive SQL analytics, independent Pandas validation, and Matplotlib visualization. The complete environment runs in GitHub Codespaces; no physical IoT hardware or local software installation is required.

## Problem statement
Urban air-quality datasets can contain many observations across locations and dates. CityPulse demonstrates a repeatable processing approach to summarize pollutant measurements and identify temporal and location-wise patterns.

## Objectives
1. Generate a reproducible synthetic air-quality dataset.
2. Implement a MapReduce aggregation using Hadoop Streaming.
3. Store and query raw and aggregated data using Hive SQL.
4. Verify the distributed-processing result independently with Pandas.
5. Visualize monthly trends and city comparisons.
6. Host and execute the project in GitHub Codespaces.

## Tools and technologies
GitHub repository and Codespaces; Java 8; Hadoop 3.3.6; Hadoop Streaming; Hive 3.1.3; embedded Apache Derby metastore; Python 3; Pandas; Matplotlib; CSV and TSV files.

## System architecture
Synthetic CSV → Mapper → key sorting/grouping by Hadoop Streaming → Reducer → aggregate TSV → Hive managed tables and SQL queries. In parallel, Pandas recomputes the aggregates for validation and generates chart-ready summaries; Matplotlib creates PNG graphs.

## Methodology
**Dataset:** deterministic generator creates 10,000 rows by default for six illustrative Indian cities over calendar year 2025. Columns: city, date, PM2.5, PM10, NO2, temperature, and humidity. Values are synthetic.

**Mapper:** reads CSV rows, derives YYYY-MM from date, and emits `city|month|pollutant<TAB>reading` for PM25, PM10, and NO2.

**Shuffle and sort:** Hadoop Streaming sorts the intermediate keys and groups values for each key. The job uses Hadoop's local framework for a single-node simulation.

**Reducer:** computes sum/count and emits city, month, pollutant, arithmetic mean, and observation count.

**Hive:** creates a database and managed raw/aggregate tables, loads the two local files, and runs five SQL analyses.

**Validation and visualization:** Pandas independently groups the source data and checks counts and means against MapReduce results within rounding tolerance. Matplotlib generates monthly PM2.5 trend and city ranking charts.

## Execution procedure
1. Upload repository contents to GitHub.
2. Create a Codespace using the supplied `.devcontainer` configuration.
3. Wait for the Java, Hadoop, Hive, and Python environment build.
4. Run `bash scripts/run_all.sh` in the Codespaces terminal.
5. Inspect `output/`, especially `output/mapreduce/part-00000`, both PNG charts, and `output/hive/hive_execution.log`.

## Expected results
The run generates 10,000 source observations, MapReduce monthly aggregates for each observed city/month/pollutant combination, two PNG graphs, two summary CSV files, and Hive query output. The Pandas validation stage should print `VALIDATION PASSED`. Exact averages depend on the deterministic generator seed and row count; with the default seed and row count, results are reproducible.

## Result interpretation
The monthly trend graph compares synthetic PM2.5 means over time. The city ranking graph compares weighted overall synthetic PM2.5 means. Hive query outputs provide ranked city-month values, the highest city per month, pollutant comparisons, a sample threshold filter, and a missing-value count. These results demonstrate the processing workflow only and must not be interpreted as actual environmental conditions.

## Limitations
This is a single-node Hadoop local-mode simulation, not a multi-node cluster. The dataset is synthetic. Hive uses an embedded Derby metastore and local file loading; HDFS daemons and a remote metastore are not part of this setup. It is not a production or real-time monitoring deployment.

## Conclusion
CityPulse demonstrates the end-to-end concepts of a Big Data analytics pipeline in a reproducible, browser-based environment. Hadoop Streaming performs aggregation, Hive supports SQL-based analysis, and Pandas validation and Matplotlib visualization provide independent checks and interpretable outputs.
