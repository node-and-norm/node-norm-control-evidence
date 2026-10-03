"""Detect missing, unexpected or changed artifacts relative to a saved manifest."""
import argparse
import hashlib
import json
from pathlib import Path


def verify(root):
    root = Path(root)
    manifest = json.loads((root / 'manifest.json').read_text())
    expected = manifest['artifacts']
    actual = {str(f.relative_to(root)): hashlib.sha256(f.read_bytes()).hexdigest()
              for f in root.rglob('*') if f.is_file() and f != root / 'manifest.json'}
    if actual != expected:
        raise ValueError('Artifact set or content differs from recorded manifest')
    return len(actual)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('run', type=Path)
    print(verify(parser.parse_args().run))
