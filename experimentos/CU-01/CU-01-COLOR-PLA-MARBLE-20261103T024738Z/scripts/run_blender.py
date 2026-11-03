import datetime, hashlib, json, os, subprocess, sys, time
from pathlib import Path
EXP_DIR=Path(__file__).resolve().parents[1]
REPO_ROOT=Path(__file__).resolve().parents[4]
BLENDER=Path("/Applications/Blender.app/Contents/MacOS/Blender")
EXPECTED_SHA256="732d39142f70aace84432327f1b358aeb9316e75476beb9ce1e3aa2cb2748c80"
RUN_ID="CU-01-COLOR-PLA-MARBLE-20261103T024738Z"
def main():
    if len(sys.argv)<3 or sys.argv[2]!="--": raise SystemExit("usage: run_blender.py LABEL -- ARGS")
    label=sys.argv[1]; digest=hashlib.sha256(BLENDER.read_bytes()).hexdigest()
    if digest!=EXPECTED_SHA256: raise SystemExit(f"Blender hash mismatch: {digest}")
    profile=EXP_DIR/"profiles"/label
    for n in ("home","config","scripts","data","tmp"): (profile/n).mkdir(parents=True,exist_ok=True)
    env=os.environ.copy(); env.update({"HOME":str(profile/"home"),"BLENDER_USER_CONFIG":str(profile/"config"),"BLENDER_USER_SCRIPTS":str(profile/"scripts"),"BLENDER_USER_DATAFILES":str(profile/"data"),"TMPDIR":str(profile/"tmp")})
    command=[str(BLENDER),*sys.argv[3:]]; start=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds"); t=time.monotonic_ns()
    result=subprocess.run(command,cwd=REPO_ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    meta={"run_id":RUN_ID,"label":label,"command":command,"cwd":str(REPO_ROOT),"profile":str(profile),"blender_sha256":digest,"blender_version":"Blender 5.4.0 Alpha (build 745ab9a3e3c5)","start_utc":start,"end_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds"),"duration_ms":round((time.monotonic_ns()-t)/1e6,3),"exit_code":result.returncode,"log":str((EXP_DIR/"logs"/f"{label}.log").relative_to(REPO_ROOT))}
    lp=EXP_DIR/"logs"/f"{label}.log"; mp=EXP_DIR/"logs"/f"{label}.meta.json"
    if lp.exists() or mp.exists(): raise FileExistsError(label)
    lp.write_text(result.stdout+"\nRUN_META "+json.dumps(meta,sort_keys=True)+"\n"); mp.write_text(json.dumps(meta,indent=2,sort_keys=True)+"\n")
    print(result.stdout,end=""); print("RUN_META "+json.dumps(meta,sort_keys=True)); return result.returncode
if __name__=="__main__": raise SystemExit(main())
