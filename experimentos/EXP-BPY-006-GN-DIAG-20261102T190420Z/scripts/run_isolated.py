"""Execute one Blender process with a run-local user profile and complete log metadata."""
import datetime, hashlib, json, os, subprocess, sys, time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT.parents[1]
BLENDER=Path('/Applications/Blender.app/Contents/MacOS/Blender')
RUN_ID='EXP-BPY-006-GN-DIAG-20261102T190420Z'

def main():
    if len(sys.argv)<3 or sys.argv[2]!='--': raise SystemExit('usage: run_isolated.py LABEL -- BLENDER_ARGUMENTS...')
    label=sys.argv[1]; command=[str(BLENDER),*sys.argv[3:]]
    if not BLENDER.is_file(): raise SystemExit('Blender executable missing')
    profile=ROOT/'profiles'/label
    for folder in ('home','config','scripts','data','tmp'): (profile/folder).mkdir(parents=True,exist_ok=True)
    env=os.environ.copy(); env.update({'HOME':str(profile/'home'),'BLENDER_USER_CONFIG':str(profile/'config'),'BLENDER_USER_SCRIPTS':str(profile/'scripts'),'BLENDER_USER_DATAFILES':str(profile/'data'),'TMPDIR':str(profile/'tmp')})
    version=subprocess.run([str(BLENDER),'--version'],cwd=PROJECT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    version_line=next((line.strip() for line in version.stdout.splitlines() if line.strip().startswith('Blender ')),'UNAVAILABLE')
    start=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds'); tick=time.monotonic_ns()
    if version.returncode==0: result=subprocess.run(command,cwd=PROJECT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    else: result=subprocess.CompletedProcess(command,version.returncode,version.stdout)
    duration=round((time.monotonic_ns()-tick)/1e6,3); end=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds')
    log=ROOT/'logs'/(label+'.log'); meta_path=ROOT/'logs'/(label+'.meta.json')
    if log.exists() or meta_path.exists(): raise SystemExit('Refusing to overwrite existing log: '+label)
    meta={'run_id':RUN_ID,'label':label,'command':command,'cwd':str(PROJECT),'profile_isolated':str(profile),'blender_version':version_line,'version_command_exit_code':version.returncode,'blender_executable':str(BLENDER),'blender_executable_sha256':hashlib.sha256(BLENDER.read_bytes()).hexdigest(),'start_utc':start,'end_utc':end,'duration_ms':duration,'exit_code':result.returncode,'log':str(log.relative_to(PROJECT))}
    log.write_text('VERSION_COMMAND_OUTPUT\n'+version.stdout+'\nEXPERIMENT_PROCESS_OUTPUT\n'+result.stdout+'\nRUN_META '+json.dumps(meta,sort_keys=True)+'\n',encoding='utf-8')
    meta_path.write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
    print(result.stdout,end=''); print('RUN_META '+json.dumps(meta,sort_keys=True))
    return result.returncode

if __name__=='__main__': raise SystemExit(main())
