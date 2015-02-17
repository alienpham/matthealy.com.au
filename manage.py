#!/usr/bin/env python
import os

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]


from app import create_app
from flask.ext.script import Manager, Shell

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)

def make_shell_context():
    return dict(app=app)

manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def fix_blank_entry_type():
    """Fix the empty entry_type records."""
    entries = Entry.query.all()
    for entry in entries:
        if entry.entry_type is None:
            entry.entry_type = 1

if __name__ == '__main__':
    manager.run()
