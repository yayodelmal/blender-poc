"""Run one Blender process with an isolated user profile and capture provenance."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
BLENDER = Path('/Applications/Blender.app/Contents/MacOS/Blender')
EXPECTED_SHA256 = '732d39142f70aace84432327f1b358aeb9316e75476beb9ce1e3aa2cb2748c80'
RUN_ID = 'EXP-BPY-006-A-CANARY-20261102T212457Z'


def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='milliseconds')


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ('build', 'validate'):
        raise SystemExit('usage: run_isolated.py {build|validate} LABEL [arguments...]')
    mode, label, *args = sys.argv[1:]
    digest = sha256(BLENDER)
    if digest != EXPECTED_SHA256:
        raise SystemExit(f'BLENDER_HASH_MISMATCH expected={EXPECTED_SHA256} observed={digest}')

    profile = ROOT / 'profiles' / label
    home = profile / 'home'
    temp = profile / 'tmp'
    config = profile / 'config'
    scripts = profile / 'scripts'
    datafiles = profile / 'datafiles'
    extensions = profile / 'extensions'
    for directory in (home, temp, config, scripts, datafiles, extensions):
        directory.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env.update({
        'HOME': str(home),
        'TMPDIR': str(temp),
        'TMP': str(temp),
        'TEMP': str(temp),
        'XDG_CONFIG_HOME': str(config),
        'BLENDER_USER_CONFIG': str(config),
        'BLENDER_USER_SCRIPTS': str(scripts),
        'BLENDER_USER_DATAFILES': str(datafiles),
        'BLENDER_USER_EXTENSIONS': str(extensions),
    })

    if mode == 'build':
        if len(args) != 1:
            raise SystemExit('build expects output .blend path')
        command = [str(BLENDER), '--background', '--factory-startup', '--disable-autoexec',
                   '--python-exit-code', '1', '--python', str(ROOT / 'scripts/build_A_canary.py'),
                   '--', 'A', args[0]]
    else:
        if len(args) != 2:
            raise SystemExit('validate expects input .blend path and output JSON path')
        command = [str(BLENDER), '--background', '--factory-startup', '--disable-autoexec',
                   '--python-exit-code', '1', '--python', str(ROOT / 'scripts/validate_canary.py'),
                   '--', args[0], args[1]]

    version = subprocess.run([str(BLENDER), '--version'], cwd=ROOT, env=env,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    version_text = version.stdout.decode('utf-8', errors='replace')
    started = utc_now()
    t0 = time.monotonic()
    result = subprocess.run(command, cwd=ROOT, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, check=False)
    elapsed_ms = round((time.monotonic() - t0) * 1000, 3)
    ended = utc_now()
    log_path = ROOT / 'logs' / f'{label}.log'
    meta_path = ROOT / 'logs' / f'{label}.meta.json'
    log_path.write_bytes(result.stdout)
    metadata = {
        'run_id': RUN_ID,
        'label': label,
        'mode': mode,
        'command': command,
        'cwd': str(ROOT),
        'blender_executable': str(BLENDER),
        'blender_sha256': digest,
        'version_command': [str(BLENDER), '--version'],
        'version_exit_code': version.returncode,
        'version_output': version_text,
        'profile': str(profile),
        'environment_overrides': {k: env[k] for k in (
            'HOME', 'TMPDIR', 'TMP', 'TEMP', 'XDG_CONFIG_HOME',
            'BLENDER_USER_CONFIG', 'BLENDER_USER_SCRIPTS',
            'BLENDER_USER_DATAFILES', 'BLENDER_USER_EXTENSIONS')},
        'start_utc': started,
        'end_utc': ended,
        'duration_ms': elapsed_ms,
        'exit_code': result.returncode,
        'log': str(log_path.relative_to(ROOT)),
    }
    meta_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + '\n')
    sys.stdout.buffer.write(result.stdout)
    print(f'PROCESS_META {meta_path.relative_to(ROOT)}')
    print(f'PROCESS_RESULT mode={mode} label={label} exit_code={result.returncode}')
    raise SystemExit(result.returncode)


if __name__ == '__main__':
    main()
