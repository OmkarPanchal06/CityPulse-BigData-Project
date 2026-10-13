import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_mapper_emits_three_pollutants():
    sample='city,date,pm25,pm10,no2,temperature_c,humidity_pct\nPune,2025-02-01,10,20,5,30,50\n'
    p=subprocess.run([sys.executable,str(ROOT/'scripts/mapper.py')],input=sample,text=True,capture_output=True,check=True)
    assert len(p.stdout.strip().splitlines())==3
    assert 'Pune|2025-02|PM25' in p.stdout
def test_reducer_mean():
    sample='Pune|2025-02|PM25\t10\nPune|2025-02|PM25\t20\n'
    p=subprocess.run([sys.executable,str(ROOT/'scripts/reducer.py')],input=sample,text=True,capture_output=True,check=True)
    assert p.stdout.strip()=='Pune\t2025-02\tPM25\t15.000\t2'
