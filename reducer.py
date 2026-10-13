#!/usr/bin/env python3
"""Hadoop Streaming reducer: calculate mean and count for each sorted key."""
import sys
current=None; total=0.0; count=0

def emit(key, total, count):
    if key is not None and count:
        city,month,pollutant=key.split('|',2)
        print(f'{city}\t{month}\t{pollutant}\t{total/count:.3f}\t{count}')

for line in sys.stdin:
    line=line.rstrip('\n')
    if '\t' not in line: continue
    key,raw=line.split('\t',1)
    try: value=float(raw)
    except ValueError: continue
    if key!=current:
        emit(current,total,count); current=key; total=0.0; count=0
    total+=value; count+=1
emit(current,total,count)
