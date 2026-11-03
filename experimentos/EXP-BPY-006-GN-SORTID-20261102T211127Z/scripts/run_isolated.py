"""Run isolated Blender processes for the explicit multi-input sort-id diagnostic."""
import datetime,hashlib,json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PROJECT=ROOT.parents[1]
BLENDER=Path('/Applications/Blender.app/Contents/MacOS/Blender')
RUN_ID='EXP-BPY-006-GN-SORTID-20261102T211127Z'
EXPECTED_SHA='732d39142f70aace84432327f1b358aeb9316e75476beb9ce1e3aa2cb2748c80'
def main():
    if len(sys.argv)<3 or sys.argv[2]!='--': raise SystemExit('usage: run_isolated.py LABEL -- BLENDER_ARGS...')
    label=sys.argv[1]; command=[str(BLENDER),*sys.argv[3:]]
    if not BLENDER.is_file(): raise SystemExit('Pinned Blender executable missing')
    exe_sha=hashlib.sha256(BLENDER.read_bytes()).hexdigest()
    if exe_sha!=EXPECTED_SHA: raise SystemExit('Executable SHA differs from ADR-0002; refusing run')
    profile=ROOT/'profiles'/label
    for x in ('home','config','scripts','data','tmp'): (profile/x).mkdir(parents=True,exist_ok=True)
    env=os.environ.copy(); env.update({'HOME':str(profile/'home'),'BLENDER_USER_CONFIG':str(profile/'config'),'BLENDER_USER_SCRIPTS':str(profile/'scripts'),'BLENDER_USER_DATAFILES':str(profile/'data'),'TMPDIR':str(profile/'tmp')})
    ver=subprocess.run([str(BLENDER),'--version'],cwd=PROJECT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    ver_line=next((x.strip() for x in ver.stdout.splitlines() if x.strip().startswith('Blender ')),'UNAVAILABLE')
    start=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds'); tick=time.monotonic_ns()
    res=subprocess.run(command,cwd=PROJECT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True) if ver.returncode==0 else subprocess.CompletedProcess(command,ver.returncode,ver.stdout)
    end=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds'); duration=round((time.monotonic_ns()-tick)/1e6,3)
    log=ROOT/'logs'/(label+'.log'); mp=ROOT/'logs'/(label+'.meta.json')
    if log.exists() or mp.exists(): raise SystemExit('Refusing to overwrite '+label)
    meta={'run_id':RUN_ID,'label':label,'command':command,'cwd':str(PROJECT),'blender_version':ver_line,'blender_executable':str(BLENDER),'blender_executable_sha256':exe_sha,'profile_isolated':str(profile),'version_command_exit_code':ver.returncode,'start_utc':start,'end_utc':end,'duration_ms':duration,'exit_code':res.returncode,'log':str(log.relative_to(PROJECT))}
    log.write_text('VERSION_OUTPUT\n'+ver.stdout+'\nPROCESS_OUTPUT\n'+res.stdout+'\nRUN_META '+json.dumps(meta,sort_keys=True)+'\n',encoding='utf-8'); mp.write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
    print(res.stdout,end=''); print('RUN_META '+json.dumps(meta,sort_keys=True)); return res.returncode
if __name__=='__main__': raise SystemExit(main())
