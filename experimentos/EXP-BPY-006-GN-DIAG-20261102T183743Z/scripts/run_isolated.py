"""Run this diagnostic's pinned Blender binary with an isolated local profile."""
import datetime, hashlib, json, os, subprocess, sys, time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT.parents[1]
BLENDER=Path('/Applications/Blender.app/Contents/MacOS/Blender')
RUN_ID='EXP-BPY-006-GN-DIAG-20261102T183743Z'

def main():
    if len(sys.argv)<3 or sys.argv[2]!='--': raise SystemExit('usage: run_isolated.py LABEL -- BLENDER_ARGS...')
    label=sys.argv[1]; cmd=[str(BLENDER),*sys.argv[3:]]
    if not BLENDER.is_file(): raise SystemExit('Pinned Blender executable not found')
    profile=ROOT/'profiles'/label
    for part in ('home','config','scripts','data','tmp'): (profile/part).mkdir(parents=True,exist_ok=True)
    env=os.environ.copy(); env.update({'HOME':str(profile/'home'),'BLENDER_USER_CONFIG':str(profile/'config'),'BLENDER_USER_SCRIPTS':str(profile/'scripts'),'BLENDER_USER_DATAFILES':str(profile/'data'),'TMPDIR':str(profile/'tmp')})
    version=subprocess.run([str(BLENDER),'--version'],cwd=PROJECT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    start=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds'); t=time.monotonic_ns()
    result=subprocess.run(cmd,cwd=PROJECT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    duration=round((time.monotonic_ns()-t)/1e6,3); end=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds')
    meta={'run_id':RUN_ID,'label':label,'command':cmd,'cwd':str(PROJECT),'profile':str(profile),'blender_version_first_line':version.stdout.splitlines()[0] if version.stdout else 'UNAVAILABLE','blender_version_exit_code':version.returncode,'blender_executable':str(BLENDER),'blender_executable_sha256':hashlib.sha256(BLENDER.read_bytes()).hexdigest(),'start_utc':start,'end_utc':end,'duration_ms':duration,'exit_code':result.returncode,'log':str((ROOT/'logs'/(label+'.log')).relative_to(PROJECT))}
    log=ROOT/'logs'/(label+'.log'); mp=ROOT/'logs'/(label+'.meta.json')
    if log.exists() or mp.exists(): raise SystemExit('Refusing to overwrite an existing run log: '+label)
    log.write_text('BLENDER_VERSION_OUTPUT\n'+version.stdout+'\nPROCESS_OUTPUT\n'+result.stdout+'\nRUN_META '+json.dumps(meta,sort_keys=True)+'\n',encoding='utf-8')
    mp.write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
    print(result.stdout,end=''); print('RUN_META '+json.dumps(meta,sort_keys=True))
    return result.returncode

if __name__=='__main__': raise SystemExit(main())
