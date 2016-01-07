from flask import render_template, flash, redirect, session, url_for, request, g, current_app, Response, abort
from datetime import datetime, timedelta
from . import blog
from .. import pages
from slugify import slugify
from werkzeug.contrib.atom import AtomFeed

@blog.route('/', methods=['GET'])
def index():

    latest = sorted(pages, reverse=True, key=lambda p: p.meta['timestamp'])

    return render_template("blog/index.html",title='Blog',posts=latest[:5])

@blog.route('/post/list/', methods=['GET'])
def archives():

    posts = (p for p in pages)
    posts = sorted(posts, reverse=True, key=lambda p: p.meta['timestamp'])

    return render_template("blog/archives.html",title='Posts',posts=posts)

@blog.route('/post/tagged/<tag>/', methods=['GET'])
def view_tagged_posts(tag):

    tagged = [p for p in pages if tag in p.meta.get('tags', [])]

    posts = sorted(tagged, reverse=True, key=lambda p: p.meta['timestamp'])

    if not posts:
        abort(404)

    return render_template("blog/post.html",posts=posts,title=tag)

@blog.route('/post/<slug>/', methods=['GET'])
def view_post(slug):

    post = pages.get(slug)

    if not post:
        abort(404)

    return render_template("blog/post.html",posts=[post],title=post.meta['title'])

@blog.route('/recent.atom')
def recent_feed():

    feed = AtomFeed('Recent Articles',
                    feed_url='http://www.matthealy.com.au/blog/recent.atom', url='http://www.matthealy.com.au')

    latest = sorted(pages, reverse=True, key=lambda p: p.meta['timestamp'])

    for post in latest[:15]:
        feed.add(post.meta['title'], unicode(post.html),
                 content_type='html',
                 author=post.meta['author'],
                 url='http://www.matthealy.com.au/blog/post/'+post.meta['slug']+'/',
                 updated=post.meta['timestamp'])

    return feed.get_response()
