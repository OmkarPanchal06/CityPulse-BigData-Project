#!/usr/bin/env python3
"""Validate MapReduce aggregates with pandas and create reproducible charts."""
from pathlib import Path
import pandas as pd
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
data=pd.read_csv(ROOT/'data/citypulse_synthetic.csv',parse_dates=['date'])
rows=[]
for line in (ROOT/'output/mapreduce/part-00000').read_text().splitlines():
    c,m,p,a,n=line.split('\t'); rows.append((c,m,p,float(a),int(n)))
mr=pd.DataFrame(rows,columns=['city','month','pollutant','avg_value','record_count'])
# Independent pandas calculation from original observations.
long=data.melt(id_vars=['city','date'],value_vars=['pm25','pm10','no2'],var_name='pollutant',value_name='reading')
long['month']=long.date.dt.strftime('%Y-%m'); long['pollutant']=long.pollutant.map({'pm25':'PM25','pm10':'PM10','no2':'NO2'})
check=long.groupby(['city','month','pollutant']).reading.agg(['mean','count']).reset_index()
merged=mr.merge(check,on=['city','month','pollutant'],suffixes=('_mr','_pd'))
if len(merged)!=len(check) or not (merged.record_count==merged['count']).all() or not ((merged.avg_value-merged['mean']).abs()<0.0011).all():
    raise SystemExit('VALIDATION FAILED: MapReduce results differ from Pandas.')
mr.to_csv(ROOT/'output/monthly_pollution.csv',index=False)
# City-level pollutant summary
mr.groupby(['city','pollutant'],as_index=False).avg_value.mean().to_csv(ROOT/'output/city_pollutant_summary.csv',index=False)
# chart 1: PM2.5 monthly average by city
pm=mr[mr.pollutant=='PM25'].pivot(index='month',columns='city',values='avg_value').sort_index()
ax=pm.plot(figsize=(11,6),marker='o'); ax.set_title('CityPulse: Monthly mean PM2.5 (synthetic data)'); ax.set_xlabel('Month'); ax.set_ylabel('PM2.5 (illustrative units)'); ax.grid(True,alpha=.3); plt.tight_layout(); plt.savefig(ROOT/'output/monthly_pm25_by_city.png',dpi=160); plt.close()
# chart 2: city ranking
rank=mr[mr.pollutant=='PM25'].groupby('city').apply(lambda x:(x.avg_value*x.record_count).sum()/x.record_count.sum(),include_groups=False).sort_values()
ax=rank.plot(kind='barh',figsize=(9,5)); ax.set_title('CityPulse: Overall weighted mean PM2.5'); ax.set_xlabel('PM2.5 (illustrative units)'); plt.tight_layout(); plt.savefig(ROOT/'output/city_pm25_ranking.png',dpi=160); plt.close()
print(f'VALIDATION PASSED: {len(merged)} city-month-pollutant aggregates matched Pandas.')
print('\nTop PM2.5 city-month combinations:')
print(mr[mr.pollutant=='PM25'].sort_values('avg_value',ascending=False).head(10).to_string(index=False))
