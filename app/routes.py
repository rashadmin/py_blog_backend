from app import app
from flask_login import current_user,login_user,logout_user,login_required
@app.route('/')
@app.route('/index',methods=['GET','POST'])
@login_required
def home():
    return 'Hello World'


@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return 'home'
    return 'login form'

@app.route('/logout')
def logout():
    logout_user()
    return 'logout'
