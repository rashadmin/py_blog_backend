from app import app
from flask import request,url_for
from werkzeug.urls import url_parse
from flask_login import current_user,login_user,logout_user,login_required
from app.models import User,Post 
from app import db
form = []
@app.route('/')
@app.route('/index',methods=['GET','POST'])
@login_required
def home():
    post = Post(body=form.post.data, author=current_user)
    db.session.add(post)
    db.session.commit()
    return 'Hello World'


@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return 'home'
    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
        return 'index'
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('index')
    return 'login form'

@app.route('/logout')
def logout():
    logout_user()
    return 'logout'

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return 'user'


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    return ...