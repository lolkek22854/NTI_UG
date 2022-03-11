from flask import *
from data import db_session
from flask_login.login_manager import *
from flask_login.utils import *
from data.forms import *
from data.user import User
from data.history import Action
from data.bin import Tank
from data.st import Status
from flask import request
import datetime
import json
from flask_admin import Admin, expose, AdminIndexView
from flask_cors import CORS, cross_origin
from flask_admin.contrib.sqla import ModelView
from utils.hash import *
from utils.adminView import *
import os


class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.is_authenticated:
            if current_user.role == 1488:
                session = db_session.create_session()
                tanks = session.query(Tank).all()
                t = []
                for e in tanks:
                    t.append((e.type, e.resources, e.status))
                st = session.query(Status).all()
                if st[0].status == 1: servo='OK'
                else: servo='NOT WORKING'
                if st[1].status == 1: sc='OK'
                else: sc='NOT WORKING'
                if st[2].status == 1: sd='OK'
                else: sd='NOT WORKING'
                return self.render('admin/index.html', plastic=t[0][1], glass=t[1][1], paper=t[2][1], servo=servo, sensorsc=sc, sensorsd=sd)
            else:
                return redirect('/')
        else:
            return redirect('/')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init('db/data.sqlite')
admin = Admin(app, name='popich', template_mode='bootstrap3', index_view=MyHomeView())
admin.add_view(UserView(User, db_session.create_session()))
admin.add_view(ActionView(Action, db_session.create_session()))


@app.before_first_request
def create_db():
    db_session.global_init('db/data.sqlite')
    session = db_session.create_session()
    if not session.query(User).filter(User.role==1488).first():
        print('no mama')
        user = User(login='admin', card_id=0, points=0, role=1488)
        user.set_password('admin')
        session.add(user)
        session.commit()
    for i in range(3):
        print(session.query(Tank).filter(Tank.type == i).first())
        if not session.query(Tank).filter(Tank.type == i).first():
            tank = Tank(type=i, resources=0, status=100)
            session.add(tank)
            session.commit()
    for i in range(3):
        print(session.query(Status).filter(Status.type == i).first())
        if not session.query(Status).filter(Status.type == i).first():
            st = Status(type=i, status=1)
            session.add(st)
            session.commit()
    session.commit()


@login_manager.user_loader
def load_user(user_id):
    db_session.global_init('db/data.sqlite')
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
def index():
    # db_session.global_init("db/data.sqlite")
    if not current_user.is_authenticated:
        return redirect('/non_authorization')
    elif current_user.role == 1488:
        return redirect('/admin')
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
@cross_origin()
def send_data():
    print(request)
    print(request.form)
    print(request.data)
    form = json.loads(request.data.decode('utf8').replace("'", '"'))
    # print(form)
    if form['RequestType'] == 'add_points':
        session = db_session.create_session()
        user = session.query(User).filter(User.card_id == form['cardID']).first()
        if user:
            user.points += int(form['value'])
            act = Action(user_id=user.id, action='зачислены баллы: ' + str(form['value']),
                         time=str(datetime.datetime.now())[:-7], user=user.login)
            act1 = Action(user_id=user.id, action='Утилизация мусора в бак: '+['стекло', 'бумага', 'пластик'][int(form['tank'])],
                          time=str(datetime.datetime.now())[:-7], user=user.login)
            session.merge(user)
            tank = session.query(Tank).filter(Tank.type == form['tank']).first()
            tank.resources += 10
            session.merge(tank)
            session.add(act)
            session.add(act1)
            session.commit()
            return {'response': 'ok'}
        return {'response': 'id invalid'}
    else:
        session = db_session.create_session()
        user = session.query(User).filter(User.card_id == form['cardID']).first()
        if user:
            return {'response': 'ok', 'user': str(user.role)}
    return {'response': 'ok', 'user': -1}


@app.route('/app', methods=['GET', 'POST'])
def check_id():
    form = dict(request.json)
    print(form)
    session = db_session.create_session()
    for i in range(3):
        st = session.query(Status).filter(Status.type == i).first()
        st.status = int(form.get(['is_servo', 'is_rgb', 'is_near'][i]))
        session.merge(st)
    session.commit()
    return {'response': 'ok'}


# @app.errorhandler(404)
# def not_found(error):
#     return render_template('404.html')


def main():
    db_session.global_init("db/data.sqlite")
    app.run()


if __name__ == '__main__':
    main()
