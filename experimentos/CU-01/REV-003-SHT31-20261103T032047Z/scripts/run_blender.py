"""Run an isolated, hash-pinned Blender process and preserve command metadata."""
import datetime, hashlib, json, os, subprocess, sys, time
from pathlib import Path
EXP_DIR=Path(__file__).resolve().parents[1]
REPO_ROOT=Path(__file__).resolve().parents[4]
BLENDER=Path('/Applications/Blender.app/Contents/MacOS/Blender')
EXPECTED_SHA256='732d39142f70aace84432327f1b358aeb9316e75476beb9ce1e3aa2cb2748c80'
RUN_ID='CU-01-REV-003-20261103T032047Z'
def sha256(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for block in iter(lambda:f.read(1<<20),b''):h.update(block)
 return h.hexdigest()
def main():
 if len(sys.argv)<3 or sys.argv[2]!='--':raise SystemExit('usage: run_blender.py LABEL -- BLENDER_ARGUMENTS...')
 label=sys.argv[1];observed=sha256(BLENDER)
 if observed!=EXPECTED_SHA256:raise SystemExit(f'Blender hash mismatch: {observed}')
 command=[str(BLENDER),*sys.argv[3:]];profile=EXP_DIR/'profiles'/label
 log=EXP_DIR/'logs'/f'{label}.log';meta_path=EXP_DIR/'logs'/f'{label}.meta.json'
 if log.exists() or meta_path.exists():raise FileExistsError(f'refusing to overwrite {label} logs')
 for child in ('home','config','scripts','data','tmp'):(profile/child).mkdir(parents=True,exist_ok=True)
 env=os.environ.copy();env.update({'HOME':str(profile/'home'),'BLENDER_USER_CONFIG':str(profile/'config'),'BLENDER_USER_SCRIPTS':str(profile/'scripts'),'BLENDER_USER_DATAFILES':str(profile/'data'),'TMPDIR':str(profile/'tmp')})
 start=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds');t=time.monotonic_ns()
 result=subprocess.run(command,cwd=REPO_ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 end=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds');duration=(time.monotonic_ns()-t)/1e6
 meta={'run_id':RUN_ID,'label':label,'command':command,'cwd':str(REPO_ROOT),'profile':str(profile),'blender_sha256':observed,'blender_version':'Blender 5.4.0 Alpha (build 745ab9a3e3c5)','start_utc':start,'end_utc':end,'duration_ms':round(duration,3),'exit_code':result.returncode,'log':str((EXP_DIR/'logs'/f'{label}.log').relative_to(REPO_ROOT))}
 log.write_text(result.stdout+'\nRUN_META '+json.dumps(meta,sort_keys=True)+'\n',encoding='utf-8');meta_path.write_text(json.dumps(meta,indent=2,sort_keys=True)+'\n',encoding='utf-8')
 print(result.stdout,end='');print('RUN_META '+json.dumps(meta,sort_keys=True));return result.returncode
if __name__=='__main__':raise SystemExit(main())
