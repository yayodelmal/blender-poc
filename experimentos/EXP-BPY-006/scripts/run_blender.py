"""Run the pinned Blender binary with an EXP-BPY-006-local profile and timing log."""
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
BLENDER = Path('/Applications/Blender.app/Contents/MacOS/Blender')
RUN_ID = 'EXP-BPY-006-20261102T175526Z'


def main():
    if len(sys.argv) < 3 or sys.argv[2] != '--':
        raise SystemExit('usage: python3 run_blender.py LABEL -- BLENDER_ARGUMENTS...')
    label = sys.argv[1]
    command = [str(BLENDER), *sys.argv[3:]]
    profile = ROOT / 'profiles' / label
    for name in ('home', 'config', 'scripts', 'data', 'tmp'):
        (profile / name).mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update({
        'HOME': str(profile / 'home'),
        'BLENDER_USER_CONFIG': str(profile / 'config'),
        'BLENDER_USER_SCRIPTS': str(profile / 'scripts'),
        'BLENDER_USER_DATAFILES': str(profile / 'data'),
        'TMPDIR': str(profile / 'tmp'),
    })
    start_utc = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds')
    start_ns = time.monotonic_ns()
    result = subprocess.run(command, cwd=ROOT.parent.parent, env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    duration_ms = (time.monotonic_ns() - start_ns) / 1_000_000
    end_utc = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds')
    log_path = ROOT / 'logs' / (label + '.log')
    meta_path = ROOT / 'logs' / (label + '.meta.json')
    metadata = {
        'run_id': RUN_ID, 'label': label, 'command': command,
        'cwd': str(ROOT.parent.parent), 'profile': str(profile),
        'start_utc': start_utc, 'end_utc': end_utc,
        'duration_ms': round(duration_ms, 3), 'exit_code': result.returncode,
        'log': str(log_path.relative_to(ROOT.parent.parent)),
    }
    log_path.write_text(result.stdout + '\nRUN_META ' + json.dumps(metadata, sort_keys=True) + '\n', encoding='utf-8')
    meta_path.write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')
    print(result.stdout, end='')
    print('RUN_META ' + json.dumps(metadata, sort_keys=True))
    return result.returncode


if __name__ == '__main__':
    raise SystemExit(main())
