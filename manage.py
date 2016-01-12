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
from flask.ext.migrate import Migrate, MigrateCommand
from flask_flatpages import FlatPages
from flask_frozen import Freezer

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)

pages = FlatPages(app)

freezer = Freezer(app)

def make_shell_context():
    return dict(app=app, pages=pages)

manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def freeze():
    """Freeze the site to a set of static HTML files."""
    app.config['DEBUG'] = False
    freezer.freeze()

if __name__ == '__main__':
    manager.run()
