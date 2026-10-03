import tempfile
import unittest
from pathlib import Path
from run_container import command

class LauncherGuards(unittest.TestCase):
    def test_rejects_mutable_image_or_other_repository(self):
        for name in ('python:3.12-slim', '', 'other@sha256:'+'a'*64):
            with self.assertRaises(ValueError):
                command(name, Path('/tmp/test'))

    def test_bounds_mounts_and_disables_network(self):
        from run_container import ROOT
        result = command('python@sha256:'+'a'*64, Path('/tmp/test'))
        self.assertIn('--network=none', result)
        self.assertIn('--read-only', result)
        mounts = [result[i+1] for i, value in enumerate(result) if value == '--mount']
        self.assertEqual(mounts, [f'type=bind,source={ROOT},target=/app,readonly',
                                  'type=bind,source=/tmp/test,target=/output'])
        self.assertNotIn('--privileged', result)
