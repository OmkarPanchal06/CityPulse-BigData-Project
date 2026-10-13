#!/usr/bin/env python3
"""Hadoop Streaming mapper: emit city|month|pollutant -> reading."""
import csv, sys
from datetime import datetime
for row in csv.DictReader(sys.stdin):
    try:
        city=row['city'].strip().replace('|','_').replace('\t',' ')
        month=datetime.strptime(row['date'].strip(),'%Y-%m-%d').strftime('%Y-%m')
        for field,label in (('pm25','PM25'),('pm10','PM10'),('no2','NO2')):
            raw=row.get(field,'')
            if raw is None or not raw.strip(): continue
            value=float(raw)
            if value>=0: print(f'{city}|{month}|{label}\t{value}')
    except (ValueError,KeyError,TypeError):
        continue
