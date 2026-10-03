"""Authored service fixture. Each invocation is a separate worker process."""
import argparse
import json
from pathlib import Path
import sqlite3


def initialize(path):
    with Path(path).open('xb'):
        pass
    with sqlite3.connect(path) as db:
        db.execute('CREATE TABLE control (id INTEGER PRIMARY KEY CHECK (id=1), stopped INTEGER NOT NULL)')
        db.execute('INSERT INTO control VALUES (1, 0)')
        db.execute('CREATE TABLE effects (id INTEGER PRIMARY KEY, request_id TEXT NOT NULL)')


def perform(path, commands, persist_stop=True, deduplicate=True):
    # Opening a missing store must fail, never silently construct an empty service.
    uri = Path(path).resolve().as_uri() + '?mode=rw'
    with sqlite3.connect(uri, uri=True) as db:
        state = db.execute('SELECT stopped FROM control WHERE id=1').fetchone()
        if state is None:
            raise ValueError('Missing control state')
        stopped = bool(state[0])
        events = []
        for command in commands:
            with db:
                if command == 'stop':
                    stopped = True
                    if persist_stop:
                        db.execute('UPDATE control SET stopped=1 WHERE id=1')
                    events.append({'event': 'stop_response', 'accepted': True})
                elif command == 'commit':
                    # One logical request is deliberately replayed by the runner.
                    prior = db.execute('SELECT COUNT(*) FROM effects WHERE request_id=?', ('request-1',)).fetchone()[0]
                    if not stopped and not (deduplicate and prior):
                        db.execute('INSERT INTO effects(request_id) VALUES (?)', ('request-1',))
                    events.append({'event': 'commit_response', 'received': True})
                else:
                    raise ValueError('Unknown command')
    return events


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('database', type=Path)
    parser.add_argument('commands', nargs='+', choices=['stop', 'commit'])
    parser.add_argument('--volatile-stop', action='store_true')
    parser.add_argument('--allow-duplicates', action='store_true')
    args = parser.parse_args()
    print(json.dumps(perform(args.database, args.commands, not args.volatile_stop, not args.allow_duplicates)))
