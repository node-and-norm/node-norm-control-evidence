"""Read-only observation of simulated downstream records; no scenario labels."""
import sqlite3
from pathlib import Path


def observe(database_path):
    uri = Path(database_path).resolve().as_uri() + '?mode=ro'
    with sqlite3.connect(uri, uri=True) as connection:
        rows = connection.execute('SELECT action, internal_record, recipient_record FROM outcome').fetchall()
    if len(rows) != 1 or rows[0][0] not in ('prevented', 'executed'):
        raise ValueError('Missing or invalid terminal outcome; run cannot be scored')
    return dict(zip(('action', 'internal_record', 'recipient_record'), rows[0]))
