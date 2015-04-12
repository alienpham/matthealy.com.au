from flask import render_template, flash, redirect, session, url_for, request, g, current_app, Response, abort
from flask.ext.login import login_user, logout_user, current_user, login_required
from datetime import datetime, timedelta
from . import blog
from ..models import User, Post
from .. import db, lm
from .forms import LoginForm, PostForm
import markdown

@blog.route('/', methods=['GET'])
def index():

    posts = Post.query.filter_by(deleted=None).all()

    return render_template("blog/index.html",title='Blog',posts=posts)

@blog.route('/post/add', methods=['GET','POST'])
@login_required
def add_post():

    form = PostForm()

    if form.validate_on_submit():
        content = form.content.data
        content_html = markdown.markdown(form.content.data)
        post = Post(user_id = g.user.id, title=form.title.data, content=content, content_html=content_html, timestamp = datetime.utcnow())
        db.session.add(post)
        db.session.commit()
        flash('Your post was successfully published.')
        return redirect(url_for('blog.view_post', post_id = post.id))

    return render_template("blog/edit.html",title='Add Post',form=form)

@blog.route('/post/<int:post_id>', methods=['GET'])
def view_post(post_id):

    posts = Post.query.filter_by(id = post_id, deleted=None).all()

    return render_template("blog/post.html",posts=posts)

@blog.route('/post/<int:post_id>/edit', methods=['GET','POST'])
@login_required
def edit_post(post_id):

    form = PostForm()

    if form.validate_on_submit():

        post = Post.query.filter_by(id = post_id, user_id = g.user.id, deleted=None).first_or_404()

        post.title = form.title.data
        post.content = form.content.data
        post.content_html = markdown.markdown(form.content.data)

        db.session.add(post)
        db.session.commit()

        flash('Your post was successfully updated.')

        return redirect(url_for('blog.view_post', post_id = post.id))

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
            return redirect(request.args.get('next') or url_for('main.index'))
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

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@blog.before_request
def before_request():
    g.user = current_user
