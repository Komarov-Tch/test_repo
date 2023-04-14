from flask import Flask
from static.data import db_session
from static.data.users import User
from static.data.news import News
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '838uj idjfksjfkljd 903wkdl'

def main():
    db_session.global_init('static/db/news.db')
#    app.run()
#    user = User()
#    user.name = 'Пользователь 3'
#    user.about = 'Биография пользователя 3'
#    user.email = 'email3@почта.ру'
    db_sess = db_session.create_session()
#    db_sess.add(user)
#    db_sess.commit()

    db_sess.query(News).filter(News.id == 3).delete()
    db_sess.commit()
    

if __name__ == '__main__':
    main()

