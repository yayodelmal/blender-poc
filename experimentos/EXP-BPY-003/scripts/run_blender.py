"""Run one Blender command with an isolated experiment-local profile and durable timing metadata."""
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
BLENDER = Path('/Applications/Blender.app/Contents/MacOS/Blender')


def main():
    if len(sys.argv) < 3 or sys.argv[2] != '--':
        raise SystemExit('usage: python3 run_blender.py LABEL -- BLENDER_ARGUMENTS...')
    label = sys.argv[1]
    command = [str(BLENDER), *sys.argv[3:]]
    profile = ROOT / 'logs' / ('profile_' + label)
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
    start = time.monotonic_ns()
    completed = subprocess.run(command, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    duration_ms = (time.monotonic_ns() - start) / 1_000_000
    end_utc = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds')
    log_path = ROOT / 'logs' / (label + '.log')
    meta_path = ROOT / 'logs' / (label + '.meta.json')
    log_path.write_text(completed.stdout + f'\nRUN_META start_utc={start_utc} end_utc={end_utc} duration_ms={duration_ms:.3f} exit_code={completed.returncode}\n', encoding='utf-8')
    metadata = {
        'label': label,
        'run_id': 'EXP-BPY-003-20261102T144300Z',
        'command': command,
        'cwd': str(ROOT),
        'profile': str(profile),
        'start_utc': start_utc,
        'end_utc': end_utc,
        'duration_ms': round(duration_ms, 3),
        'exit_code': completed.returncode,
        'log': str(log_path.relative_to(ROOT)),
    }
    meta_path.write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')
    print(completed.stdout, end='')
    print('RUN_META ' + json.dumps(metadata, sort_keys=True))
    return completed.returncode


if __name__ == '__main__':
    raise SystemExit(main())
