from flask import *
from data import db_session
from flask_login.login_manager import *
from flask_login.utils import *
from data.forms import *
from data.user import User
from data.history import Action
from flask import request
import datetime
from utils.hash import *
import random

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_session.global_init('db/data.sqlite')
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect('/non_authorization')
    session = db_session.create_session()
    u = session.query(Action).filter(Action.user_id == current_user.id)
    act = []
    for e in u:
        act.append((e.action, e.time))
    session.commit()
    act = sorted(act, key=lambda x: x[1], reverse=True)
    labels = ('событие', 'время')
    return render_template('index.html', username=current_user.login, points=current_user.points,
                           src='../static/images/frog.jpg', content=act, labels=labels)


@app.route('/non_authorization')
def non_authorization():
    return render_template('non_authorization.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('user_reg.html', title='Registration',
                                   form=form,
                                   message="Passwords are not the same")
        session = db_session.create_session()
        if session.query(User).filter(User.login == form.login.data).first():
            return render_template('user_reg.html', title='Registration',
                                   form=form,
                                   message="This user already exists")
        user = User(
            login=form.login.data,
            card_id=form.card_id.data,
            points=0,
            role=1,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        login_user(user, remember=True)
        return redirect("/")
    return render_template('user_reg.html', title='Registration', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.login == form.login.data).first()
        session.commit()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('user_log.html', title='Authorization',
                               message="Wrong login or password",
                               form=form)
    return render_template('user_log.html', title='Authorization', form=form)


@app.route('/add_points', methods=['GET', 'POST'])
def add_points():
    print(dict(request.form))

    return {'response': 'ok'}


@app.route('/logout')
@login_required
def logout():
    if not current_user.is_authenticated:
        return redirect('/non_authorization')
    logout_user()
    return redirect("/")


@app.route('/send_data', methods=['GET', 'POST'])
def send_data():
    print(dict(request.form))
    form = dict(request.form)
    session = db_session.create_session()
    user = session.query(User).filter(User.card_id == form['id']).first()
    if user:
        user.points += int(form['points'])
        act = Action(user_id=user.id, action='зачислены баллы: ' + str(form['points']),
                     time=str(datetime.datetime.now())[:-7])
        session.merge(user)
        session.add(act)
        session.commit()
        return {'response': 'ok'}
    return {'response': 'id invalid'}


@app.route('/check_id', methods=['GET', 'POST'])
def check_id():
    print(dict(request.form))
    form = dict(request.form)
    session = db_session.create_session()
    user = session.query(User).filter(User.card_id == form['id']).first()
    if user:
        return {'response': 'ok', 'user': str(user.role)}
    return {'response': 'ok', 'user': -1}


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')


def main(*args):
    db_session.global_init("db/data.sqlite")
    print(args)
    print(len(args))
    print(*args)
    app.run(host='0.0.0.0', port=args[0]['SERVER_PORT'])



if __name__ == '__main__':
    main()
