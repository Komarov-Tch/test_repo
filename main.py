import json

from flask import Flask, render_template, redirect
from static.forms.loginform import LoginForm
from static.forms.user import RegisterForm
from static.data.news import News
from static.data.users import User
from static.data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'JALIDUJOISD&*ASUJD:*(*)(Ipi9043iokfd;'


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message='Пароли не совпадают'
                                   )
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message='Пользователь с таким email существует'
                                   )
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.about = form.about.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html',
                           title='Регистрация',
                           form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизаци', form=form)


@app.route('/success')
def success():
    params = {}
    params['title'] = 'Авторизация'
    params['text'] = 'Авторизация прошла успешно'
    return render_template('success.html', **params)


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    params = {}
    params['title'] = 'Главная страница'
    params['news'] = news
    return render_template('index.html', **params)


@app.route('/odd_even/<int:num>')
def odd_even(num):
    params = {}
    params['title'] = 'Четное-нечетное'
    params['num'] = num
    return render_template('odd_even.html', **params)


@app.route('/news')
def news():
    with open('news.json', 'rt', encoding='utf-8') as f:
        news_list = json.load(f)
    params = {}
    params['title'] = 'Новости погоды'
    params['news'] = news_list
    return render_template('news.html', **params)


if __name__ == '__main__':
    db_session.global_init('static/db/news.db')
    app.run(port=8080, host='127.0.0.1')
