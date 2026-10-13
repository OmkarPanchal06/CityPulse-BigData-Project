#!/usr/bin/env python3
"""Run Hadoop Streaming locally; use Hadoop's local framework (single-node simulation)."""
import os, subprocess, sys, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/citypulse_synthetic.csv'; OUT=ROOT/'output/mapreduce'

def main():
    hadoop=shutil.which('hadoop'); jar=os.environ.get('HADOOP_STREAMING_JAR')
    if not hadoop: raise SystemExit('hadoop command not found. Rebuild the Codespace container.')
    if not jar:
        candidates=list(Path(os.environ.get('HADOOP_HOME','/opt/hadoop')).glob('share/hadoop/tools/lib/hadoop-streaming-*.jar'))
        if not candidates: raise SystemExit('Hadoop Streaming JAR not found under HADOOP_HOME.')
        jar=str(candidates[0])
    if not DATA.exists(): raise SystemExit(f'Missing {DATA}; run python scripts/generate_data.py first.')
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.parent.mkdir(exist_ok=True)
    cmd=[hadoop,'jar',jar,'-D','mapreduce.framework.name=local','-D','fs.defaultFS=file:///','-D','mapreduce.job.reduces=1',
         '-files',f'{ROOT}/scripts/mapper.py,{ROOT}/scripts/reducer.py',
         '-input',str(DATA),'-output',str(OUT),'-mapper','python3 mapper.py','-reducer','python3 reducer.py']
    print('Executing:', ' '.join(cmd)); subprocess.run(cmd,cwd=ROOT,check=True)
    part=OUT/'part-00000'
    if not part.exists(): raise SystemExit('MapReduce completed but part-00000 was not created.')
    print(f'MapReduce output: {part}')
if __name__=='__main__': main()
