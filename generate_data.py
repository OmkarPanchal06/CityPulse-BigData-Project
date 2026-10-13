#!/usr/bin/env python3
"""Generate deterministic synthetic city air-quality observations."""
import argparse, csv, random
from datetime import date, timedelta
from pathlib import Path

CITIES = {
    "Mumbai": (38, 82, 31), "Delhi": (92, 145, 48),
    "Pune": (29, 64, 24), "Bengaluru": (25, 52, 19),
    "Chennai": (31, 69, 27), "Kolkata": (55, 103, 36),
}
FIELDS = ["city", "date", "pm25", "pm10", "no2", "temperature_c", "humidity_pct"]

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--rows',type=int,default=10000)
    p.add_argument('--seed',type=int,default=42)
    p.add_argument('--output',default='data/citypulse_synthetic.csv')
    a=p.parse_args(); rng=random.Random(a.seed)
    start=date(2025,1,1); end=date(2025,12,31); days=(end-start).days+1
    path=Path(a.output); path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
        for i in range(a.rows):
            city=rng.choice(list(CITIES)); pm25,pm10,no2=CITIES[city]
            d=start+timedelta(days=rng.randrange(days))
            seasonal=1.25 if d.month in (11,12,1) else (0.85 if d.month in (6,7,8) else 1.0)
            w.writerow({'city':city,'date':d.isoformat(),
                'pm25':round(max(1,rng.gauss(pm25*seasonal,pm25*.22)),2),
                'pm10':round(max(2,rng.gauss(pm10*seasonal,pm10*.20)),2),
                'no2':round(max(1,rng.gauss(no2, no2*.18)),2),
                'temperature_c':round(rng.uniform(18,39),1),
                'humidity_pct':round(rng.uniform(25,95),1)})
    print(f'Generated {a.rows:,} synthetic records: {path}')
if __name__=='__main__': main()
