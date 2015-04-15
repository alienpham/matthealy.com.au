from flask import render_template, flash, redirect, session, url_for, request, g, current_app, Response, abort
from flask.ext.login import login_user, logout_user, current_user, login_required
from datetime import datetime, timedelta
from . import blog
from ..models import User, Post
from .. import db, lm
from .forms import LoginForm, PostForm
from slugify import slugify
from werkzeug.contrib.atom import AtomFeed

@blog.route('', methods=['GET'])
def index():

    posts = Post.query.filter_by(deleted=None).order_by(Post.timestamp.desc()).all()

    return render_template("blog/index.html",title='Blog',posts=posts)

@blog.route('/post/list', methods=['GET'])
def archives():

    posts = Post.query.filter_by(deleted=None).order_by(Post.timestamp.desc()).all()

    return render_template("blog/archives.html",title='Posts',posts=posts)

@blog.route('/post/add', methods=['GET','POST'])
@login_required
def add_post():

    form = PostForm()

    if form.validate_on_submit():
        slug = slugify(form.title.data)
        post = Post(user_id = g.user.id, title=form.title.data, content=form.content.data, timestamp = datetime.utcnow(), slug = slug)
        db.session.add(post)
        db.session.commit()
        flash('Your post was successfully published.')
        return redirect(url_for('blog.view_post', slug = post.slug))

    return render_template("blog/edit.html",title='Add Post',form=form)

@blog.route('/post/<slug>', methods=['GET'])
def view_post(slug):

    posts = Post.query.filter_by(slug = slug, deleted=None).all()

    if not posts:
        abort(404)

    return render_template("blog/post.html",posts=posts,title='Post')

@blog.route('/post/<int:post_id>/edit', methods=['GET','POST'])
@login_required
def edit_post(post_id):

    form = PostForm()

    if form.validate_on_submit():

        post = Post.query.filter_by(id = post_id, user_id = g.user.id, deleted=None).first_or_404()

        post.title = form.title.data
        post.content = form.content.data
        post.slug = slugify(form.title.data)

        db.session.add(post)
        db.session.commit()

        flash('Your post was successfully updated.')

        return redirect(url_for('blog.view_post', slug = post.slug))

    post = Post.query.filter_by(id = post_id, user_id = g.user.id, deleted=None).first_or_404()

    form.title.data = post.title
    form.content.data = post.content
    form.id.data = post.id

    return render_template("blog/edit.html",title='Edit Post',post=post,form=form)

@blog.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('blog.index'))
        flash('Invalid username or password.')

    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('blog.index'))

    if request.args.get('next'):
        session['next_url'] = request.args.get('next')

    return render_template('blog/login.html', form=form, title='Log In')

@blog.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('blog.index'))

@blog.route('/recent.atom')
def recent_feed():
    feed = AtomFeed('Recent Articles',
                    feed_url=request.url, url=request.url_root)

    posts = Post.query.filter_by(deleted=None).order_by(Post.timestamp.desc()).limit(15).all()

    for post in posts:
        feed.add(post.title, unicode(post.content_html),
                 content_type='html',
                 author=post.user.first_name,
                 url=url_for('blog.view_post',slug = post.slug, _external=True),
                 updated=post.timestamp)
    return feed.get_response()

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@blog.before_request
def before_request():
    g.user = current_user
