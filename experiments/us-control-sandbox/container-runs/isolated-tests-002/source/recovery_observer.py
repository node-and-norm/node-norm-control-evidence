"""Read committed effects through a separate read-only connection."""
from pathlib import Path
import sqlite3


def observe(path):
    with sqlite3.connect(Path(path).resolve().as_uri() + '?mode=ro', uri=True) as db:
        effects = db.execute('SELECT request_id FROM effects ORDER BY id').fetchall()
    return {'effect_count': len(effects), 'request_ids': [row[0] for row in effects]}
