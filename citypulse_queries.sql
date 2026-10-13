CREATE DATABASE IF NOT EXISTS citypulse;
USE citypulse;

DROP TABLE IF EXISTS air_quality_raw;
CREATE TABLE air_quality_raw (
  city STRING, date STRING, pm25 DOUBLE, pm10 DOUBLE, no2 DOUBLE,
  temperature_c DOUBLE, humidity_pct DOUBLE
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ('skip.header.line.count'='1');
LOAD DATA LOCAL INPATH '__RAW_CSV_PATH__' OVERWRITE INTO TABLE air_quality_raw;

DROP TABLE IF EXISTS monthly_pollution;
CREATE TABLE monthly_pollution (
  city STRING, month STRING, pollutant STRING,
  avg_value DOUBLE, record_count BIGINT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE;
LOAD DATA LOCAL INPATH '__MR_OUTPUT_PATH__' OVERWRITE INTO TABLE monthly_pollution;

-- Query 1: Monthly PM2.5 ranking.
SELECT city, month, ROUND(avg_value, 2) AS avg_pm25, record_count
FROM monthly_pollution WHERE pollutant='PM25' ORDER BY avg_value DESC LIMIT 20;

-- Query 2: Highest PM2.5 city in each month.
SELECT month, city, avg_value FROM (
  SELECT month, city, avg_value,
         ROW_NUMBER() OVER (PARTITION BY month ORDER BY avg_value DESC) AS rn
  FROM monthly_pollution WHERE pollutant='PM25'
) ranked WHERE rn=1 ORDER BY month;

-- Query 3: Compare pollutants by city.
SELECT city, pollutant, ROUND(AVG(avg_value),2) AS mean_monthly_level
FROM monthly_pollution GROUP BY city,pollutant ORDER BY city,pollutant;

-- Query 4: Illustrative threshold only; not official AQI or health advice.
SELECT city,month,avg_value FROM monthly_pollution
WHERE pollutant='PM25' AND avg_value>=60 ORDER BY avg_value DESC;

-- Query 5: Missing-value check (empty CSV fields are interpreted as NULL).
SELECT COUNT(*) AS rows,
       SUM(CASE WHEN pm25 IS NULL THEN 1 ELSE 0 END) AS missing_pm25
FROM air_quality_raw;
