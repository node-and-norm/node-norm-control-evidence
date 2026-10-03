"""Run inside the test container; inspect only declared restrictions."""
import argparse
import errno
import json
import os
from pathlib import Path
import socket


def blocked_write(path):
    try:
        with path.open('x') as handle:
            handle.write('isolation probe')
    except OSError as exc:
        return {'blocked': exc.errno in (errno.EROFS, errno.EACCES, errno.EPERM), 'errno': exc.errno}
    else:
        path.unlink()
        return {'blocked': False, 'errno': None}


def main(output):
    status = dict(line.split(':', 1) for line in Path('/proc/self/status').read_text().splitlines() if ':' in line)
    sock = socket.socket()
    sock.settimeout(2)
    try:
        code = sock.connect_ex(('198.51.100.1', 443))
    except OSError as exc:
        code = exc.errno
    finally:
        sock.close()
    source = blocked_write(Path('/app/.source-write-probe'))
    root = blocked_write(Path('/usr/.root-write-probe'))
    interfaces = sorted(p.name for p in Path('/sys/class/net').iterdir())
    cgroup = Path('/sys/fs/cgroup')
    details = {
        'uid': os.geteuid(), 'source_write': source, 'root_write': root,
        'interfaces': interfaces, 'connect_errno': code,
        'capabilities_effective': status['CapEff'].strip(),
        'no_new_privileges': status['NoNewPrivs'].strip(),
        'memory_max': (cgroup/'memory.max').read_text().strip(),
        'pids_max': (cgroup/'pids.max').read_text().strip(),
        'cpu_max': (cgroup/'cpu.max').read_text().strip(),
    }
    checks = {
        'non_root': details['uid'] != 0,
        'source_read_only': source['blocked'],
        'root_read_only': root['blocked'],
        'loopback_only': interfaces == ['lo'],
        'external_network_unreachable': code == errno.ENETUNREACH,
        'capabilities_dropped': int(details['capabilities_effective'], 16) == 0,
        'no_new_privileges': details['no_new_privileges'] == '1',
        'memory_bounded': details['memory_max'] == '268435456',
        'processes_bounded': details['pids_max'] == '64',
        'cpu_bounded': details['cpu_max'] == '100000 100000',
    }
    # Successful exclusive creation also verifies the allowed output mount.
    with output.open('x') as handle:
        json.dump({'checks': checks, 'details': details, 'passed': all(checks.values())}, handle, indent=2)
        handle.write('\n')
    return 0 if all(checks.values()) else 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    raise SystemExit(main(parser.parse_args().output))
