#!/usr/bin/env python
import os

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]


from app import create_app, db
from app.models import User, Post, Tag
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)

migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Tag=Tag)

manager.add_command("shell", Shell(make_context=make_shell_context))

manager.add_command('db', MigrateCommand)

@manager.command
def generate_sitemap():
    """Generate an updated sitemap."""
    basedir = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(basedir, 'app/static/sitemap.xml')
    target = open(filename,'w')

    target.write("""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>http://www.matthealy.com.au/</loc>
  </url>
  <url>
    <loc>http://www.matthealy.com.au/services</loc>
  </url>
  <url>
    <loc>http://www.matthealy.com.au/portfolio</loc>
  </url>
  <url>
    <loc>http://www.matthealy.com.au/contact</loc>
  </url>
  <url>
    <loc>http://www.matthealy.com.au/blog</loc>
  </url>
  <url>
    <loc>http://www.matthealy.com.au/blog/post/list</loc>
  </url>""")

    posts = Post.query.filter_by(deleted=None).order_by(Post.timestamp.asc()).all()
    for post in posts:
        target.write("\n  <url>\n    <loc>http://www.matthealy.com.au/blog/post/" + post.slug + "</loc>\n  </url>")

    tags = Tag.query.all()
    for tag in tags:
        target.write("\n  <url>\n    <loc>http://www.matthealy.com.au/blog/post/tagged/" + tag.name + "</loc>\n  </url>")

    target.write("\n</urlset>")

    target.close()

if __name__ == '__main__':
    manager.run()
