"""Launch only an explicitly pinned Python image with restricted container settings."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent


def command(image, output, docker='docker', context=None, suite='basic'):
    if not re.fullmatch(r'python@sha256:[0-9a-f]{64}', image):
        raise ValueError('Provide an official Python image by sha256 digest; tags are not accepted')
    if suite not in ('basic', 'recovery', 'tests'):
        raise ValueError('Unknown suite')
    entry = ['-m', 'unittest', 'discover', '-s', 'tests', '-v'] if suite == 'tests' else [('recovery.py' if suite == 'recovery' else 'sandbox.py'), '--output', '/output/result']
    prefix = [docker] + (['--context', context] if context else [])
    return prefix + ['run', '--rm', '--network=none', '--read-only', '--cap-drop=ALL',
            '--security-opt=no-new-privileges', '--pids-limit=64', '--memory=256m', '--cpus=1',
            '--user', f'{os.getuid()}:{os.getgid()}',
            '--tmpfs', '/tmp:rw,nosuid,nodev,noexec,size=64m,mode=1777',
            '--mount', f'type=bind,source={ROOT},target=/app,readonly',
            '--mount', f'type=bind,source={output},target=/output',
            '--workdir=/app', image, 'python', '-B'] + entry


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--context')
    parser.add_argument('--image')
    parser.add_argument('--run-name')
    parser.add_argument('--suite', choices=['basic', 'recovery', 'tests'], default='basic')
    args = parser.parse_args()
    docker = shutil.which('docker')
    prefix = [docker] + (['--context', args.context] if args.context else []) if docker else []
    if args.check:
        if docker:
            result = subprocess.run(prefix + ['info', '--format', '{{.ServerVersion}}'], capture_output=True, text=True)
            ready = result.returncode == 0
        else:
            ready = False
        print(json.dumps({'docker_found': bool(docker), 'daemon_ready': ready,
                          'isolation_verified': False, 'pinned_image_required': True}))
        return 0 if ready else 2
    if not docker:
        parser.error('Docker is unavailable; no fallback to unisolated execution')
    if not args.run_name or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}', args.run_name):
        parser.error('A unique alphanumeric --run-name is required')
    destination = ROOT/'container-runs'/args.run_name
    argv = command(args.image or '', destination, docker, args.context, args.suite)
    destination.mkdir(parents=True, exist_ok=False)
    (destination/'launch.json').write_text(json.dumps({'command': argv, 'image': args.image,
        'status': 'attempted; container restrictions require verification'}, indent=2)+'\n')
    result = subprocess.run(argv, capture_output=True, text=True)
    (destination/'stdout.txt').write_text(result.stdout)
    (destination/'stderr.txt').write_text(result.stderr)
    (destination/'exit.json').write_text(json.dumps({'exit_code': result.returncode})+'\n')
    return result.returncode

if __name__ == '__main__':
    raise SystemExit(main())
